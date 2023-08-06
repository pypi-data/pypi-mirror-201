from typing import Tuple, Dict
import gc
import random
import pandas as pd

from gpforecaster.model.gpf import GPF
from gpforecaster.utils.logger import Logger
from gpforecaster import __version__


def select_hyperparameters(
    learning_rates,
    weight_decays,
    scheduler_types,
    gamma_rates,
    inducing_points_percs,
    patiences,
):
    return (
        random.choice(learning_rates),
        random.choice(weight_decays),
        random.choice(scheduler_types),
        random.choice(gamma_rates),
        random.choice(inducing_points_percs),
        random.choice(patiences),
    )


def create_and_train_model(
    dataset_name,
    hierarchical_data,
    inducing_points_perc,
    gp_type,
    learning_rate,
    weight_decay,
    scheduler_type,
    gamma_rate,
    patience,
):
    gpf = GPF(
        dataset=dataset_name,
        groups=hierarchical_data,
        inducing_points_perc=inducing_points_perc,
        gp_type=gp_type,
    )
    model, _ = gpf.train(
        lr=learning_rate,
        weight_decay=weight_decay,
        scheduler_type=scheduler_type,
        gamma_rate=gamma_rate,
        patience=patience,
    )
    return gpf, model


def clean_up_model(model, gpf):
    del model
    del gpf
    gc.collect()


def log_trial(trial, result, logger_tuning, dataset_name, gp_type):
    (
        learning_rate,
        weight_decay,
        scheduler_type,
        gamma_rate,
        inducing_points_perc,
        patience,
        val_loss,
    ) = result
    logger_tuning.info(
        f"Trial: {trial}, "
        f"Algorithm: gpf_{gp_type}, "
        f"Version: {__version__}, "
        f"Dataset: {dataset_name}, "
        f"Best hyperparameters: learning rate = {learning_rate}, "
        f"weight decay = {weight_decay}, "
        f"scheduler = {scheduler_type}, "
        f"gamma = {gamma_rate}, "
        f"inducing points percentage = {inducing_points_perc}, "
        f"patience = {patience}"
        f"Validation loss: {val_loss}"
    )


def trial_generator(
    dataset_name,
    hierarchical_data,
    num_trials,
    gp_type,
    learning_rates,
    weight_decays,
    scheduler_types,
    gamma_rates,
    inducing_points_percs,
    patiences,
):
    for _ in range(num_trials):
        (
            learning_rate,
            weight_decay,
            scheduler_type,
            gamma_rate,
            inducing_points_perc,
            patience,
        ) = select_hyperparameters(
            learning_rates,
            weight_decays,
            scheduler_types,
            gamma_rates,
            inducing_points_percs,
            patiences,
        )

        gpf, model = create_and_train_model(
            dataset_name,
            hierarchical_data,
            inducing_points_perc,
            gp_type,
            learning_rate,
            weight_decay,
            scheduler_type,
            gamma_rate,
            patience,
        )

        val_loss = gpf.val_losses[-1]
        clean_up_model(model, gpf)

        yield learning_rate, weight_decay, scheduler_type, gamma_rate, inducing_points_perc, patience, val_loss


def find_best_hyperparameters(results):
    return list(pd.DataFrame(results).dropna().sort_values(by=6).iloc[0].to_numpy())


def log_best_hyperparameters(
    best_hyperparameters, dataset_name, gp_type, logger_tuning
):
    logger_tuning.info(
        f"BEST -> "
        f"Algorithm: gpf_{gp_type}, "
        f"Version: {__version__}, "
        f"Dataset: {dataset_name}, "
        f"Best hyperparameters: learning rate = {best_hyperparameters[0]}, "
        f"weight decay: {best_hyperparameters[1]}, "
        f"scheduler: {best_hyperparameters[2]}, "
        f"gamma: {best_hyperparameters[3]}, "
        f"inducing points percentage: {best_hyperparameters[4]}, "
        f"patience: {best_hyperparameters[5]}, "
        f"Validation loss: {best_hyperparameters[6]}"
    )


def optimize_hyperparameters(
    dataset_name: str,
    hierarchical_data: Dict,
    num_trials: int = 40,
    gp_type: str = "exact",
    learning_rates: Tuple[float] = (1e-2, 1e-3),
    weight_decays: Tuple[float] = (1e-3, 1e-4, 1e-5),
    scheduler_types: Tuple[str] = ("step", "exponential", "cosine", "none"),
    gamma_rates: Tuple[float] = (0.1, 0.9, 0.95, 0.8),
    inducing_points_percs: Tuple[float] = (0.75,),
    patiences: Tuple[int] = (4, 6, 8, 10),
) -> Tuple[float, float, str, float, int, float]:
    logger_tuning = Logger(
        "hyperparameter_tuning", dataset=f"{dataset_name}_hypertuning", to_file=True
    )
    results = []

    for trial, result in enumerate(
        trial_generator(
            dataset_name,
            hierarchical_data,
            num_trials,
            gp_type,
            learning_rates,
            weight_decays,
            scheduler_types,
            gamma_rates,
            inducing_points_percs,
            patiences,
        )
    ):
        log_trial(trial, result, logger_tuning, dataset_name, gp_type)
        results.append(result)

    best_hyperparameters = find_best_hyperparameters(results)
    log_best_hyperparameters(best_hyperparameters, dataset_name, gp_type, logger_tuning)

    return best_hyperparameters
