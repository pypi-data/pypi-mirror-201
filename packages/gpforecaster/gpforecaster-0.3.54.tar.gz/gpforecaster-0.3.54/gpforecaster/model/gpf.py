from datetime import timedelta
import os
import time
import psutil
from typing import Dict, Union, Tuple, Optional, Any

import numpy as np
import torch
import gpytorch
import pickle
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from torch.utils.data import DataLoader, TensorDataset
from gpytorch.models import IndependentModelList
from sklearn.preprocessing import StandardScaler
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.likelihoods import LikelihoodList
from gpytorch.mlls import SumMarginalLogLikelihood
from gpytorch.kernels import (
    ScaleKernel,
    RBFKernel,
    PeriodicKernel,
)

from gpforecaster import __version__
from gpforecaster.utils.logger import Logger
from gpforecaster.model.gp import ExactGPModel, SparseGPModel, SvgGPModel
from gpforecaster.model.mlls import SumVariationalELBO
from gpforecaster.model.mean_functions import PiecewiseLinearMean
from gpforecaster.results.calculate_metrics import CalculateResultsBottomUp


class GPF:
    """
    A class for training and forecasting hierarchical time series datasets with Gaussian Process models.

    Parameters:
        dataset: Name of the dataset.
        groups: Dictionary containing the train and predict groups.
        input_dir: Directory where input files are stored
        n_samples: Number of samples to draw from the posterior distribution
        store_prediction_samples: Whether to store the prediction samples
        store_prediction_points: Whether to store the prediction points.
        log_dir: Directory where log files are stored. Default is '.'.
        inducing_points_perc: Percentage of inducing points to use.
        gp_type: Type of GP: exact, sparse, etc

    Attributes:
        dataset (str): Name of the dataset.
        groups (dict): Dictionary containing the train and predict groups.
        input_dir (str): Directory where input files are stored.
        timer_start (float): Start time of the training process.
        wall_time_train (float): Wall time for training.
        wall_time_predict (float): Wall time for prediction.
        wall_time_total (float): Total wall time.
        n_samples (int): Number of samples to draw from the posterior distribution.
        store_prediction_samples (bool): Whether to store the prediction samples.
        store_prediction_points (bool): Whether to store the prediction points.
        train_x (torch.Tensor): Tensor with the training data input.
        train_y (torch.Tensor): Tensor with the training data output.
        test_x (torch.Tensor): Tensor with the test data input.
        test_y (torch.Tensor): Tensor with the test data output.
        original_data (np.ndarray): Orignal dataset
        original_data_transformed (np.ndarray): Orignal dataset transformed
        n_train (int): Number of training samples
        n_test (int): Number of testing samples
        s (int): Number of time series
        losses (list): List of losses during training.
        val_losses (list): List of validation losses during training.
        model_version (str): Version of the model.
        logger_train (Logger): Logger for the training process.
        logger_metrics (Logger): Logger for the metrics.
    """

    def __init__(
        self,
        dataset: str,
        groups: dict,
        input_dir: str = "./",
        n_samples: int = 500,
        store_prediction_samples: bool = False,
        store_prediction_points: bool = False,
        log_dir: str = ".",
        inducing_points_perc: float = 0.75,
        gp_type: str = "exact",
    ):
        self.dataset = dataset
        self.groups = groups
        self.input_dir = input_dir
        self.timer_start = time.time()
        self.wall_time_train = None
        self.wall_time_predict = None
        self.wall_time_total = None
        self.original_data = groups["predict"]["data_matrix"]

        self.groups, self.scaler = self._preprocess(self.groups)
        self.n_samples = n_samples
        self.store_prediction_samples = store_prediction_samples
        self.store_prediction_points = store_prediction_points

        self.train_x = torch.from_numpy(np.asarray(groups["train"]["x_values"]))
        self.train_x = self.train_x.type(torch.Tensor)
        self.train_x = self.train_x.unsqueeze(-1)
        self.train_y = torch.from_numpy(groups["train"]["data"]).to(torch.float32)

        self.test_x = torch.from_numpy(
            np.asarray(groups["predict"]["x_values"][-self.groups["h"] :])
        )
        self.test_x = self.test_x.type(torch.Tensor)
        self.test_x = self.test_x.unsqueeze(-1)
        self.test_y = torch.from_numpy(
            groups["predict"]["data_matrix"][-self.groups["h"] :]
        ).to(torch.float32)

        self.original_data_transformed = groups["predict"]["data_matrix"]

        self.n_train = groups["train"]["n"]
        self.n_predict = groups["predict"]["n"]
        self.s = groups["train"]["s"]

        self.gp_type = gp_type
        self.inducing_points = (
            torch.rand(int(inducing_points_perc * self.n_train), dtype=torch.float32)
            * self.n_train
        )
        self.inducing_points, sorted_indices = self.inducing_points.sort()
        self.losses = []
        self.val_losses = []
        self.mll = None

        self.model_version = __version__

        self.logger_train = Logger(
            "train", dataset=self.dataset, to_file=True, log_dir=log_dir
        )
        self.logger_train.info(f"GP Type: {self.gp_type}")
        self.logger_predict = Logger(
            "predict", dataset=self.dataset, to_file=True, log_dir=log_dir
        )
        self.logger_metrics = Logger(
            "metrics", dataset=self.dataset, to_file=True, log_dir=log_dir
        )

    def _preprocess(self, groups):
        scaler = StandardScaler()
        scaler.fit(self.groups["train"]["data"])
        groups["train"]["data"] = scaler.transform(groups["train"]["data"])
        groups["predict"]["data_matrix"] = scaler.transform(
            groups["predict"]["data_matrix"]
        )

        return groups, scaler

    def _dataloader(self, x, y, batch_size):
        dataset = TensorDataset(x, y)
        return DataLoader(dataset, batch_size=batch_size, shuffle=True)

    def _build_mixtures(self):
        """
        Build the mixtures matrix.

        Returns:
            known_mixtures (np.ndarray): The mixtures matrix.
            n_groups (int): number of groups.

        Example:
                Group1     |   Group2
            GP1, GP2, GP3  | GP1, GP2
            0  , 1  , 1    | 0  , 1
            1  , 0  , 0    | 1  , 0
            0  , 1, , 1    | 0  , 1
            1  , 0  , 1    | 1  , 0
        """
        idxs = []
        for k, val in self.groups["train"]["groups_idx"].items():
            idxs.append(val)

        idxs_t = np.array(idxs).T

        n_groups = np.sum(
            np.fromiter(self.groups["train"]["groups_n"].values(), dtype="int32")
        )
        known_mixtures = np.zeros((self.groups["train"]["s"], n_groups))
        k = 0
        for j in range(self.groups["train"]["g_number"]):
            for i in range(np.max(idxs_t[:, j]) + 1):
                idx_to_1 = np.where(idxs_t[:, j] == i)
                known_mixtures[:, k][idx_to_1] = 1
                k += 1

        top_level = np.ones((known_mixtures.shape[0], 1))
        known_mixtures = np.concatenate((known_mixtures, top_level), axis=1)
        n_groups += 1

        return known_mixtures, n_groups

    def _build_cov_matrices(self, random_init: bool):
        """
        Build the covariance matrices.

        Parameters:
            mixtures (np.ndarray): The mixtures matrix.

        Returns:
            covs (list): List of covariance functions.
            known_mixtures (np.ndarray): The mixtures matrix.
            n_groups (int): number of groups.
        """
        known_mixtures, n_groups = self._build_mixtures()
        covs = []
        for i in range(1, n_groups + 1):
            if random_init:
                rbf_kernel_lengthscale = torch.rand(1)
                scale_rbf_kernel_outputscale = torch.rand(1)
                periodic_kernel_lengthscale = torch.rand(1)
                scale_periodic_kernel_outputscale = torch.rand(1)
            else:
                rbf_kernel_lengthscale = torch.tensor([1.0])
                scale_rbf_kernel_outputscale = torch.tensor([0.5])
                periodic_kernel_lengthscale = torch.tensor([0.5])
                scale_periodic_kernel_outputscale = torch.tensor([1.5])

            # RBF kernel
            rbf_kernel = RBFKernel()
            rbf_kernel.lengthscale = rbf_kernel_lengthscale
            scale_rbf_kernel = ScaleKernel(rbf_kernel)
            scale_rbf_kernel.outputscale = scale_rbf_kernel_outputscale

            # Periodic Kernel
            periodic_kernel = PeriodicKernel()
            periodic_kernel.period_length = torch.tensor([self.groups["seasonality"]])
            periodic_kernel.lengthscale = periodic_kernel_lengthscale
            scale_periodic_kernel = ScaleKernel(periodic_kernel)
            scale_periodic_kernel.outputscale = scale_periodic_kernel_outputscale

            # Cov Matrix
            cov = scale_rbf_kernel + scale_periodic_kernel
            covs.append(cov)

        return covs, known_mixtures, n_groups

    def _apply_mixture_cov_matrices(self, random_init: bool):
        """
        Apply the mixture covariance matrices and create the final list of covariance functions.

        Returns:
            mixed_covs (cov): The list of mixture covariance functions.
        """
        covs, known_mixtures, n_groups = self._build_cov_matrices(random_init)

        # apply mixtures to covariances
        selected_covs = []
        mixed_covs = []
        for i in range(self.groups["train"]["s"]):
            mixture_weights = known_mixtures[i]
            for w_ix in range(n_groups):
                w = mixture_weights[w_ix]
                if w == 1.0:
                    selected_covs.append(covs[w_ix])
            mixed_cov = selected_covs[0]
            for cov in range(1, len(selected_covs)):
                mixed_cov += selected_covs[
                    cov
                ]  # because GP(cov1 + cov2) = GP(cov1) + GP(cov2)
            mixed_covs.append(mixed_cov)
            selected_covs = []  # clear out cov list

        return mixed_covs

    def _build_model(
        self, x: torch.Tensor, y: torch.Tensor, random_init: bool
    ) -> Tuple[list[GaussianLikelihood], list[ExactGPModel]]:
        """
        Build the model.

        Parameters:
            x: Measures
            y: Observations.

        Returns:
            likelihood_list: List of GP models.
            model_list: List of likelihoods.
        """
        mixed_covs = self._apply_mixture_cov_matrices(random_init)
        n_changepoints = 4
        changepoints = np.linspace(0, self.groups["train"]["n"], n_changepoints + 2)[
            1:-1
        ]

        model_list = []
        likelihood_list = []
        for i in range(self.groups["train"]["s"]):
            likelihood_list.append(GaussianLikelihood())
            if self.gp_type.startswith("exact"):
                model_list.append(
                    ExactGPModel(
                        train_x=x,
                        train_y=y[:, i],
                        likelihood=likelihood_list[i],
                        cov=mixed_covs[i],
                        changepoints=changepoints,
                        mean_func=PiecewiseLinearMean,
                    )
                )
            elif self.gp_type == "sparse":
                model_list.append(
                    SparseGPModel(
                        train_x=x,
                        train_y=y[:, i],
                        likelihood=likelihood_list[i],
                        cov=mixed_covs[i],
                        changepoints=changepoints,
                        mean_func=PiecewiseLinearMean,
                        inducing_points=self.inducing_points.to(torch.float32),
                    )
                )
            elif self.gp_type == "svg":
                model_list.append(
                    SvgGPModel(
                        train_x=x,
                        train_y=y[:, i],
                        likelihood=likelihood_list[i],
                        cov=mixed_covs[i],
                        changepoints=changepoints,
                        mean_func=PiecewiseLinearMean,
                        inducing_points=self.inducing_points,
                    )
                )

        return likelihood_list, model_list

    def early_stopping(self, patience: int):
        losses = [x for x in self.val_losses if x is not None]
        losses.reverse()
        non_decreasing = 0
        for x, y in zip(losses, losses[1:]):
            if np.round(x, 2) >= np.round(y, 2):
                non_decreasing += 1
            else:
                break

        if non_decreasing > patience:
            return True
        else:
            return False

    @staticmethod
    def _create_scheduler(
        scheduler_type: str, optimizer: torch.optim.Optimizer, epochs: int, gamma: float
    ) -> Optional[Any]:
        """
        Creates a scheduler for the learning rate of an optimizer.

        Parameters
            scheduler_type: The type of scheduler to use. One of 'step', 'exponential', 'cosine', or 'none'.
            optimizer: The optimizer for which to create the scheduler.
            epochs: The number of epochs to train the model.

        Returns
            Optional
                The created scheduler, or None if `scheduler_type` is 'none'.
        """
        if scheduler_type == "step":
            scheduler = torch.optim.lr_scheduler.StepLR(
                optimizer, step_size=10, gamma=gamma
            )
        elif scheduler_type == "exponential":
            scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=gamma)
        elif scheduler_type == "cosine":
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=epochs
            )
        else:
            scheduler = None
        return scheduler

    @staticmethod
    def _create_standard_optimizer(
        model, lr: float, weight_decay: float
    ) -> torch.optim.Adam:
        optimizer = torch.optim.Adam(
            model.parameters(), lr=lr, weight_decay=weight_decay
        )  # Includes GaussianLikelihood parameters
        return optimizer

    def _train_loop_iteration(
        self,
        epoch: int,
        model,
        likelihood,
        mll: gpytorch.mlls.MarginalLogLikelihood,
        standard_optimizer: Optional[torch.optim.Adam] = None,
        scheduler: Optional[Any] = None,
        early_stopping: bool = True,
        patience: int = 4,
        verbose: bool = True,
        track_mem: bool = False,
    ) -> Tuple[float, Optional[float]]:
        """
        Perform a single iteration of the training loop.

        Parameters:
            epoch: The current epoch number.
            model: The model to be trained.
            likelihood: The likelihood function for the model.
            mll: The marginal log-likelihood function.
            standard_optimizer: The optimizer used for training. Defaults to None.
            scheduler: The learning rate scheduler. Defaults to None.
            early_stopping: Perform early stopping. Defaults to True.
            patience: Parameter for early stopping. Defaults to 4.
            verbose: Print outputs during training. Defaults to True.
            track_mem: Track and log RAM usage. Defaults to False.

        Returns:
            Tuple[float, Optional[float]]: Tuple containing the current loss value and validation loss value (if applicable).
        """
        standard_optimizer.zero_grad()

        output = model(*model.train_inputs)
        loss = -mll(output, model.train_targets)
        self.losses.append(loss.item())

        val_loss = None
        if early_stopping and epoch % 5 == 0:
            model.eval()
            likelihood.eval()
            val_loss = self.validate(model)
            if self.early_stopping(patience=patience):
                return loss.item(), val_loss

            if verbose:
                print(
                    f"Iter {epoch} - Loss: {np.round(loss.item(), 3)}, Validation Loss: {np.round(val_loss, 3)}"
                )
            model.train()
            likelihood.train()
        elif verbose:
            print(f"Iter {epoch} - Loss: {np.round(loss.item(), 3)}")

        loss.backward()
        standard_optimizer.step()

        if scheduler:
            scheduler.step()

        if epoch % 30 == 0 and track_mem:
            self._log_memory()

        return loss.item(), val_loss

    def _log_memory(self):
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / (1024**3)
        self.logger_train.info(f"train used {mem:.3f} GB of RAM")

    def train(
        self,
        lr: float = 1e-3,
        epochs: int = 500,
        early_stopping: bool = True,
        patience: int = 4,
        weight_decay: float = 1e-4,
        verbose: bool = True,
        track_mem: bool = False,
        scheduler_type: str = "cosine",
        gamma_rate: float = 0.95,
        random_init: bool = False,
    ) -> Tuple[Optional[IndependentModelList], Optional[LikelihoodList]]:
        """
        Train the model.

        Parameters:
            lr: Learning rate.
            epochs: Number of epochs
            early_stopping: Perform early stopping
            patience: Parameter to early stopping
            weight_decay: Weight decay
            verbose: Print outputs when training
            track_mem: Track and log RAM usage
            scheduler_type: Type of scheduler to use to update the learning rate
            gamma_rate: Gamma rate for the scheduler types

        Returns:
            tuple: Tuple containing the trained model and the likelihood.
        """
        likelihood_list, model_list = self._build_model(
            x=self.train_x, y=self.train_y, random_init=random_init
        )

        model = IndependentModelList(*model_list)
        likelihood = LikelihoodList(*likelihood_list)

        self._initialize_mll(model, likelihood)
        model.train()
        likelihood.train()

        optimizer = self._create_standard_optimizer(model, lr, weight_decay)
        scheduler = self._create_scheduler(
            scheduler_type, optimizer, epochs, gamma_rate
        )

        epoch = 0
        loss = None
        val_loss = None

        for epoch in range(epochs):
            loss, val_loss = self._train_loop_iteration(
                epoch,
                model,
                likelihood,
                self.mll,
                standard_optimizer=optimizer,
                scheduler=scheduler,
                early_stopping=early_stopping,
                patience=patience,
                verbose=verbose,
                track_mem=track_mem,
            )

            if (
                early_stopping
                and val_loss is not None
                and self.early_stopping(patience=patience)
            ):
                break

        self._log_training_information(epoch, loss, val_loss)

        return model, likelihood

    def _initialize_mll(self, model, likelihood) -> None:
        if self.gp_type == "svg":
            self.mll = SumVariationalELBO(
                likelihood, model, num_data=self.train_y.size(0)
            )
        else:
            self.mll = SumMarginalLogLikelihood(likelihood, model)

    def _log_training_information(
        self, epoch: int, loss: float, val_loss: Optional[float]
    ) -> None:
        wall_time_train = time.time() - self.timer_start
        training_duration = timedelta(seconds=int(wall_time_train))

        self.logger_train.info(f"Num epochs {epoch}")
        self.logger_train.info(f"Wall time train {training_duration}")

        self.logger_train.info(f"Loss {loss:.2f}")

        if val_loss is not None:
            self.logger_train.info(f"Val Loss {val_loss:.2f}")

    def validate(self, model: IndependentModelList, random_init: bool = False) -> float:
        """
        Validate the model.

        Parameters:
            model (ExactGPModel): The GP model
            random_init: initialize the hyperparamters randomly

        Returns:
            float: The negative log likelihood of the model on the validation set.
        """
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            likelihood_list_val, model_list_val = self._build_model(
                x=self.test_x, y=self.test_y, random_init=random_init
            )
            model_val = gpytorch.models.IndependentModelList(*model_list_val)
            val_output = model(*model_val.train_inputs)
            val_loss = -self.mll(val_output, model_val.train_targets)
            self.val_losses.append(float(val_loss.item()))
        return val_loss.item()

    @staticmethod
    def _create_directory_if_not_exists(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def plot_losses(self, start_idx: int = 5):
        self._create_directory_if_not_exists("plots")

        n_iterations, val_losses_interp = self._prepare_loss_data(start_idx)

        self._plot_loss_data(n_iterations, self.losses[start_idx:], val_losses_interp)
        self._customize_plot()

        timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
        plt.savefig(
            f"./plots/gpf_{__version__}_loss_{self.dataset}_{timestamp}.pdf",
            format="pdf",
            bbox_inches="tight",
        )
        plt.show()

    def _prepare_loss_data(self, start_idx: int):
        n_iterations_total = np.arange(len(self.losses))

        val_interval = round(len(self.losses) / len(self.val_losses))
        val_indices = np.arange(0, len(self.losses), val_interval)

        interp_func = interp1d(
            val_indices,
            self.val_losses,
            kind="linear",
            fill_value="extrapolate",
        )
        val_losses_interp = interp_func(n_iterations_total)[start_idx:]

        n_iterations = n_iterations_total[start_idx:]

        return n_iterations, val_losses_interp

    @staticmethod
    def _plot_loss_data(n_iterations, train_losses, val_losses_interp):
        plt.plot(n_iterations, train_losses, label="Training Loss")
        plt.plot(n_iterations, val_losses_interp, marker="*", label="Validation Loss")

    @staticmethod
    def _customize_plot():
        plt.title("Training and Validation Losses")
        plt.xlabel("Iteration")
        plt.ylabel("Loss")
        plt.legend()

    def predict(
        self,
        model: IndependentModelList,
        likelihood: LikelihoodList,
        track_mem: bool = True,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        """
        Make predictions with the model.

        Parameters:
            model: The GP model.
            likelihood: The likelihood function.
            track_mem: Track and log RAM usage

        Returns:
            numpy.ndarray: Array of shape (n_samples, n_prediction_points, n_groups)
                containing the prediction samples.
        """
        timer_start = time.time()

        model.eval()
        likelihood.eval()

        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            test_x = torch.arange(self.groups["predict"]["n"]).type(torch.float32)
            predictions = likelihood(
                *model(*[test_x for i in range(self.groups["predict"]["s"])])
            )
            if track_mem:
                # Track RAM usage
                process = psutil.Process(os.getpid())
                mem = process.memory_info().rss / (1024**3)
                self.logger_predict.info(f"predict used {mem:.3f} GB of RAM")

        pred_mean_scaled = np.zeros((self.n_predict, self.s))
        pred_std_scaled = np.zeros((self.n_predict, self.s))
        for ts in range(self.s):
            pred_mean_scaled[:, ts] = predictions[ts].mean.detach().numpy()
            pred_std_scaled[:, ts] = np.sqrt(predictions[ts].variance.detach().numpy())

        # transform back the data
        pred_mean = pred_mean_scaled * self.scaler.scale_ + self.scaler.mean_
        pred_std = pred_std_scaled * self.scaler.scale_

        self.wall_time_predict = time.time() - timer_start
        return (pred_mean, pred_std), (pred_mean_scaled, pred_std_scaled)

    @staticmethod
    def _validate_param(param, valid_values):
        if param not in valid_values:
            raise ValueError(f"{param} is not a valid value")

    def store_results(
        self,
        res: np.ndarray,
        res_type: str,
        res_measure: str,
        track_mem: bool = True,
    ):
        """
        Store results

        Parameters:
            res: np array with the results with shape (n,s) - note that n depends of the res_type
            res_type: defines the type of results, could be 'fit_pred' to receive fitted values plus
                predictions or 'pred' to only store predictions
            res_measure: defines the measure to store, could be 'mean' or 'std'

        Returns:
            numpy.ndarray: Array of shape (n_samples, n_prediction_points, n_groups)
                containing the prediction samples.
        """
        """
        Store results, res_type should be used to define the type of results,
        could be 'fit_pred' to receive fitted values plus predictions or 'pred'
        to only store predictions
        """
        self._validate_param(res_type, ["fitpred", "pred"])
        self._validate_param(res_measure, ["mean", "std"])
        with open(
            f"{self.input_dir}results_{res_type}_{res_measure}_gp_{self.gp_type}_cov_{self.dataset}_{self.model_version}.pickle",
            "wb",
        ) as handle:
            if track_mem:
                process = psutil.Process(os.getpid())
                mem = process.memory_info().rss / (1024**3)
                self.logger_metrics.info(f"Storing results used {mem:.3f} GB of RAM")
            pickle.dump(res, handle, pickle.HIGHEST_PROTOCOL)

    def store_metrics(
        self,
        res: Dict[str, Dict[str, Union[float, np.ndarray]]],
        track_mem: bool = True,
    ):
        with open(
            f"{self.input_dir}metrics_gp_{self.gp_type}_cov_{self.dataset}_{self.model_version}.pickle",
            "wb",
        ) as handle:
            if track_mem:
                process = psutil.Process(os.getpid())
                mem = process.memory_info().rss / (1024**3)
                self.logger_metrics.info(
                    f"Storing error metrics used {mem:.3f} GB of RAM"
                )
            pickle.dump(res, handle, pickle.HIGHEST_PROTOCOL)

    def metrics(
        self,
        pred_mean: np.ndarray,
        pred_std: np.ndarray,
        track_mem: bool = True,
    ) -> Dict[str, Dict[str, Union[float, np.ndarray]]]:
        """
        Calculate evaluation metrics for the predictions.

        Parameters:
            pred_mean: Array of shape (n_prediction_points, n_series)
                containing the prediction samples.
            pred_std: Array of shape (n_prediction_points, n_series)
                containing the prediction samples.
            track_mem: Track and log RAM usage

        Returns:
            dict: Dictionary with the evaluation metrics. The keys are the metric names,
                and the values are dictionaries with the results for each group.
        """
        calc_results = CalculateResultsBottomUp(
            predictions_mean=pred_mean,
            predictions_std=pred_std,
            groups=self.groups,
            dataset=self.dataset,
        )
        res = calc_results.calculate_metrics()
        if track_mem:
            process = psutil.Process(os.getpid())
            mem = process.memory_info().rss / (1024**3)
            self.logger_metrics.info(
                f"calculating error metrics used {mem:.3f} GB of RAM"
            )
        self.wall_time_total = time.time() - self.timer_start

        res["wall_time"] = {}
        res["wall_time"]["wall_time_train"] = self.wall_time_train
        res["wall_time"]["wall_time_predict"] = self.wall_time_predict
        res["wall_time"]["wall_time_total"] = self.wall_time_total

        return res
