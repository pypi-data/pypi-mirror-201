"""
Hyper-parameter tuning with Optuna
"""

# Imports
import os
import random
from typing import List, Any, Union, Dict, Tuple
import pickle
from pathlib import Path
from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import optuna
from optuna.samplers import TPESampler
from optuna.trial import FrozenTrial
from optuna.study import MaxTrialsCallback
from optuna.trial import TrialState
from optuna.visualization import plot_contour
from optuna.visualization import plot_optimization_history
from optuna.visualization import plot_parallel_coordinate
from optuna.visualization import plot_param_importances
from sklearn.model_selection import StratifiedKFold, \
    StratifiedGroupKFold, KFold
from xgboost import XGBClassifier, XGBRegressor
from tensorflow.python.platform import build_info
from lightgbm.sklearn import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, SGDClassifier, \
    RidgeClassifier, ARDRegression, SGDRegressor
from sklearn.naive_bayes import GaussianNB
from ..utils.ml_utils import Scorer
from ..utils.df_utils import DataFrameUtils as du

import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(
    '%(log_color)s[%(levelname).1s %(log_color)s%(asctime)s] - %(log_color)s%(name)s - '
    '%(message)s')
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

"""
Author: vickyparmar
File: tuners.py
Created on: 07-11-2022, Mon, 18:36:29

Last modified by: vickyparmar
Last modified on: 31-3-2023, Fri, 17:54:07
"""


# [x] A function to read the csv and extract the parameters and return a dict
# [x] Add attributes to the list as well.
# [x] Rename 'values_*' to reflect the correct metrics
# [x] Check if objective function(s) exists
# [x] Loading objective functions
# [x] Calculate Metrics
# [x] Optimization Directions
# [x] Running Optuna Study and saving the results


# class BaseTuner
class BaseTuner:
    """
                Base class for hyperparameter
                tuning  using
                `OPTUNA
                <https://github.com/optuna/optuna>`_.
                For a detailed example on how to use
                BaseTuner, check `this
                <__init__.py>`_ out.

                Parameters
                ----------
                x: Union[pd.DataFrame, pd.Series]
                    input data
                y: Union[pd.DataFrame, pd.Series]
                    target data
                save_loc: Union[str, Path]
                    location to save the end results
                cv: Union[int, Any]
                    either an integer for StratifiedKFold
                    or StratifiedGroupKFold or any
                    cv method that has split(X,y,groups).
                    Default: 5
                group_col: str
                    name of the group column in case of
                    StratifiedGroupKFold or similar
                random_state: int
                    random initializing state for
                    reproducibility. Default: 42

                Attributes
                ----------
                trials_df: pd.DataFrame
                    a DataFrame for all trials (in case of
                    single objective)
                best_trial: FrozenTrial
                    a trial with all its attributes (single
                    objective)
                multi_trials_df: pd.DataFrame
                    a DataFrame for all trials (in case of
                    multiple objectives concatinated
                    below one another)
                best_trials: Dict
                    a dictionary of trials with all their
                    attributes (multiple objectives)

                Methods
                -------
                tune(optimization_config: Dict | None,
                max_trials_callback: int)
                    takes in the configuration for
                    study.optimize(objective,
                    optimization_config) and tunes the
                    objective function.
                    `optimization_config` must be a Dict
                    and the allowed parameters can be
                    found `here
                    <https://optuna.readthedocs.io/en/
                    stable/reference/generated/optuna.
                    study.Study.html#
                    optuna.study.Study.optimize>`_

                Raises
                ------
                ValueError
                    Raised when length of `metrics`
                    do not match the length of
                     `metrics_directions` or when
                     unexpected parameters are
                     passed.
                TypeError
                    Raised when either objective or
                    metrics contains an unsupported type

                See Also
                --------
                ClassificationTuner: Tuner for classification
                    problems `<ClassificationTuner>`_
                RegressionTuner: Tuner for regression
                    problems `<RegressionTuner>`_

                Notes
                -----
                # [v] ToDo: modify suggest_categorical in dynamic space (temp-fix -> random.choice)
                # [v] ToDo: Documentation including `Notes` and README.md

                Examples
                --------
                >>> objective = 'lr'
                >>> metrics = 'roc_auc_score'
                >>> direction = 'maximize'
                >>> cv = KFold(n_splits=3,
                                         shuffle=True,
                                         random_state=99)
                >>> optimization_config = {
                            'n_trials': 5,
                            'timeout': 3600
                        }
                >>> max_trials_callback = 5
                >>> x = pd.DataFrame() # your df
                >>> y = pd.DataFrame() # your target
                >>> tuner = BaseTuner(x, y,
                                                       objective,
                                                       'tmp/data',
                                                       metrics,
                                                       direction,
                                                       cv,
                                                       42)
                >>> tuner.tune(optimization_config,
                                        max_trials_callback)
                """

    # noinspection PyTypeChecker
    def __init__(self, x: Union[pd.DataFrame, pd.Series],
                 y: Union[pd.DataFrame, pd.Series],
                 save_loc: Union[str, Path],
                 cv: Union[int, Any] = 5, group_col: str = None,
                 random_state: int = 42):
        # noinspection PyTypeChecker
        self.x, self.y = x, y
        self.unique_length = self.y.nunique()
        self.objective_fn = None
        # noinspection PyTypeChecker
        self.save_loc = Path(save_loc)
        self.random_state = random_state
        self.cv = cv
        self.group_col = group_col
        self.cuda_build = build_info.build_info['is_cuda_build']
        self.params = []
        self.trials_df = pd.DataFrame()
        self.best_trial = None
        self.multi_trials_df = pd.DataFrame()
        self.best_trials = {}
        # noinspection PyBroadException
        try:
            self.terminal_size = os.get_terminal_size().columns
        except Exception:
            self.terminal_size = 100

    # Create and run Optuna Study
    def create_and_run_study(self, objective: Any, max_trials_callback: int,
                             direct: Union[str, List[str]], save_loc: Path,
                             **kwargs) -> Tuple[pd.DataFrame, Union[FrozenTrial, List]]:
        """
        Creating an Optuna.study.Study and
        running study.optimize(*). Optuna
        dashboard files will be saved at `save_loc`.
        `.html` files can be directly
        viewed in a browser. Or one can install
        optuna-dashboard using `pip install
        optuna-dashboard` and run `
        optuna-dashboard sqlite:///path-to-db.sqlite3`.

        Parameters
        ----------
        objective: Any
            Objective function. A callable function
            that takes in `optuna.trial.Trial` as input
            and returns either a float or multiple
            float values (usually scores or losses) to
            be optimized.
        max_trials_callback: int
            When running multiple studies, this will
            be the total number of trials for all
            the studies combined.
        direct: Union[str, List[str]]
            Direction(s) in which the score(s)/loss(es)
            will be optimized
        save_loc: Path
            Location to save the database and plots
        kwargs: Dict
            Configuration parameters for `optuna.
            study.Study.optimize`

        Returns
        -------
        tuple: Tuple[pd.DataFrame, Union[FrozenTrial, List]]
            Returns a tuple containing a DataFrame
            with all trials and a FrozenTrial containing
            all trial parameters.
        """
        print('=' * self.terminal_size)
        sampler = TPESampler(seed=self.random_state,
                             n_startup_trials=2, multivariate=True,
                             group=True)
        study_name = f"{objective.__name__}"
        save_loc.mkdir(parents=True, exist_ok=True)
        storage_name = f"sqlite:///{save_loc}/db.sqlite3"

        if isinstance(direct, str):
            study = optuna.create_study(direction=direct,
                                        pruner=optuna.pruners.MedianPruner(),
                                        sampler=sampler,
                                        study_name=study_name,
                                        storage=storage_name,
                                        load_if_exists=True)
        else:
            study = optuna.create_study(directions=direct,
                                        pruner=optuna.pruners.MedianPruner(),
                                        sampler=sampler,
                                        study_name=study_name,
                                        storage=storage_name,
                                        load_if_exists=True)
        optuna.logging.enable_default_handler()
        max_trials_callback = MaxTrialsCallback(max_trials_callback,
                                                states=(
                                                    TrialState.COMPLETE,))
        study.optimize(objective, callbacks=[max_trials_callback],
                       catch=tuple([Exception]), **kwargs)

        optimization_history = plot_optimization_history(study)
        optimization_history.write_html(f"{save_loc}/optimization_history.html")
        contour = plot_contour(study)
        contour.write_html(f"{save_loc}/contour.html")
        parallel_coordinate = plot_parallel_coordinate(study)
        parallel_coordinate.write_html(f"{save_loc}/parallel_coordinate.html")
        param_importance = plot_param_importances(study)
        param_importance.write_html(f"{save_loc}/param_importance.html")
        param_importance_duration = plot_param_importances(
            study, target=lambda t: t.duration.total_seconds(), target_name="duration"
        )
        param_importance_duration.write_html(f"{save_loc}/param_importance_duration.html")

        trials_df = study.trials_dataframe()
        if isinstance(direct, List):
            best_trial = study.best_trials
        else:
            best_trial = study.best_trial
        return trials_df, best_trial

    # Running one or multiple objectives
    def tune(self, optimization_config: Dict = None,
             max_trials_callback: int = 1000,
             directions: Union[str, List[str]] = 'maximize',
             metrics: Union[str, List[str]] = 'roc_auc_score'):
        """
        Taking the given parameters and tuning
        the objective function(s).

        Parameters
        ----------
        metrics: Union[str, List[str]]
            Metrics to optimize for the objective
            Default: 'roc_auc_score'
        directions: Union[str, List[str]]
            Directions to optimize to metrics.
            Default: 'maximize'
        optimization_config: Dict | None
            Configuration parameters for optuna.
            study.Study.optimize. Default: None
            i.e. optimization_config = {
                'n_trials': 1000,
                'timeout': 3600
            }
        max_trials_callback: int
            When running multiple studies, this will
            be the total number of trials for all
            the studies combined. Default: 1000

        Returns
        -------
        None
        """
        # Optimization config
        if optimization_config is None:
            optimization_config = {
                'n_trials': 1000,
                'timeout': 3600
            }

        # Running the study
        if isinstance(self.objective_fn, list):
            best_trials = {}
            # noinspection PyTypeChecker
            for objective in tqdm(self.objective_fn, position=0,
                                  desc="Running multiple objective functions",
                                  colour='green', total=len(self.objective_fn)):
                save_loc = self.save_loc / f"{objective.__name__}"

                trials_df, best_trial = self.create_and_run_study(objective,
                                                                  max_trials_callback,
                                                                  directions,
                                                                  save_loc,
                                                                  **optimization_config)

                self.best_trials[objective.__name__] = best_trials

                trials_df['objective'] = objective.__name__
                if isinstance(metrics, List):
                    values = [c for c in trials_df.columns if 'value' in c]
                    new_cols = dict(zip(values, metrics))
                    trials_df.rename(columns=new_cols, inplace=True)
                    # final_cols = metrics.copy()
                    # final_cols.append('objective')
                else:
                    trials_df.rename(columns={'value': metrics}, inplace=True)
                    # final_cols = [metrics, 'objective']

                self.multi_trials_df = pd.concat(
                    [self.multi_trials_df, trials_df],
                    axis=0)

                entire_df = self.create_results_df(trials_df)

                entire_df = self.reindex_columns(entire_df)
                du.save_df(entire_df, f"{save_loc}/trials_df.csv", **{'index': False})

                logger.info(
                    f"\nA DataFrame containing information on all trials and a pickle file with best_trial are"
                    f"saved at {save_loc}\n")

                best_trials[f"{objective.__name__}"] = best_trial

                self.params = []

            print("-" * self.terminal_size)
            logger.info(
                f"\nHere are the best trials for all your objective functions:\n")
            for o, t in best_trials.items():
                print("-" * self.terminal_size)
                if isinstance(metrics, List):
                    for m in t:
                        print(
                            f"Objective: {o}: best_trial_{t.index(m)}")
                        logger.info(f"\n{m}\n")
                else:
                    print(f"Objective: {o}: ")
                    logger.info(f"\n{t}\n")

            self.multi_trials_df = self.reindex_columns(self.multi_trials_df)
            du.save_df(self.multi_trials_df, f"{self.save_loc}/multi_trials_df.csv",
                       **{'index': False})

        else:
            save_loc = self.save_loc / f"{self.objective_fn.__name__}"

            trials_df, best_trial = self.create_and_run_study(
                self.objective_fn, max_trials_callback, directions,
                save_loc, **optimization_config)
            trials_df['objective'] = self.objective_fn.__name__
            if isinstance(metrics, list):
                values = [c for c in trials_df.columns if 'value' in c]
                new_cols = dict(zip(values, metrics))
                trials_df.rename(columns=new_cols, inplace=True)
            else:
                trials_df.rename(columns={'value': metrics}, inplace=True)

            entire_df = self.create_results_df(trials_df)

            entire_df = self.reindex_columns(entire_df)
            du.save_df(entire_df, f"{save_loc}/trials_df.csv", **{'index': False})

            logger.info(
                f"A DataFrame containing information on all trials and a pickle file with best_trial are "
                f"saved at -> '{save_loc}'")
            print("-" * self.terminal_size)

            if isinstance(metrics, List):
                for trial in best_trial:
                    print(
                        f"Objective: {self.objective_fn.__name__}: best_trial_{best_trial.index(trial)}")
                    logger.info(f"\n{trial}")
            else:
                logger.info(f"Objective: {self.objective_fn.__name__}:")
                print(f"\n{best_trial}\n")

            self.trials_df = entire_df
            self.best_trial = best_trial

    # Reindex columns
    @staticmethod
    def reindex_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Reordering the columns of the dataframe to make more sense.

        Parameters
        ----------
        dataframe: pd.DataFrame
            the dataframe for which to reorder index

        Returns
        -------
        dataframe: pd.Dataframe:
            the dataframe with reordered columns
        """
        number = dataframe['number']
        objective = dataframe['objective']
        datetime_start = dataframe['datetime_start']
        datetime_complete = dataframe['datetime_complete']
        duration = dataframe['duration']
        state = dataframe['state']
        dataframe.drop(['objective', 'datetime_start', 'datetime_complete',
                        'duration', 'state', 'number'], axis=1, inplace=True)
        dataframe.insert(loc=dataframe.shape[1],
                         column='datetime_start', value=datetime_start)
        dataframe.insert(loc=dataframe.shape[1],
                         column='datetime_complete', value=datetime_complete)
        dataframe.insert(loc=dataframe.shape[1],
                         column='duration', value=duration)
        dataframe.insert(loc=dataframe.shape[1],
                         column='state', value=state)
        dataframe.insert(loc=0, column='number', value=number)
        dataframe.insert(loc=1, column='objective', value=objective)

        return dataframe

    # Calculate scores with CV
    def get_scores(self, estimator: Any,
                   metric_func: Any) -> List:
        """
        Takes in an estimator, performs
        cross-validation and returns the
        score(s) / loss(es)

        Parameters
        ----------
        estimator: Any
            any estimator that has a .fit, .predict,
            and .predict_proba methods.
        metric_func: Any
            a function that takes a fitted
             estimator, x_val, y_val and
             returns the required scores

        Returns
        -------
        metrics: List
            returns the user specified metrics
        """
        scores = []
        if self.group_col is not None:
            if isinstance(self.cv, int):
                cv = StratifiedGroupKFold(n_splits=self.cv,
                                          random_state=self.random_state,
                                          shuffle=True)
            else:
                cv = self.cv
            for train, val in cv.split(self.x, self.y,
                                       self.x[self.group_col]):
                x = self.x.drop(self.group_col, axis=1, inplace=False)
                x_train, y_train = x.loc[train], self.y.loc[train]
                x_val, y_val = x.loc[val], self.y.loc[val]
                estimator.fit(x_train, y_train)
                scores.append(
                    metric_func(estimator=estimator, x=x_val,
                                y=y_val))
        else:
            if isinstance(self.cv, int):
                cv = StratifiedKFold(n_splits=self.cv,
                                     random_state=self.random_state,
                                     shuffle=True)
            else:
                cv = self.cv
            for train, val in cv.split(self.x, self.y):
                x_train, y_train = self.x.loc[train], self.y.loc[train]
                x_val, y_val = self.x.loc[val], self.y.loc[val]
                estimator.fit(x_train, y_train)
                scores.append(
                    metric_func(estimator=estimator, x=x_val,
                                y=y_val))
        return scores

    # Creating a params DataFrame
    def create_results_df(self, trials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creating a DataFrame with all params for the
        estimator

        Parameters
        ----------
        trials_df: pd.DataFrane
            trials_df received from Optuna

        Returns
        -------
        results_df: pd.DataFrame
            a resulting df with all estimator as well as
            trial parameters
        """
        pdf = pd.DataFrame(self.params)
        new_cols = [f"params_{c}" for c in pdf.columns]
        pdf.columns = new_cols
        params_cols = [col for col in trials_df.columns if col.startswith('params')]
        trials_df.drop(params_cols, axis=1, inplace=True)
        pdf = pd.concat([trials_df, pdf], axis=1)
        return pdf

    # Checking the inputs
    @staticmethod
    def verify_input(objective: Union[str, List], metrics: Union[str, List]) -> None:
        """
        Verifying whether the given inputs are in
        predefined inputs.

        Parameters
        ----------
        objective: Union[str, List]
            objective functions to check
        metrics: Union[str, List]
            metrics to check

        Returns
        -------
        None
        """
        classifiers = ['lr', 'svm', 'xgb', 'rf', 'dt', 'cat',
                       'lgbm', 'sgd', 'gnb', 'ridge']
        clf_met = ['roc_auc_score', 'accuracy_score',
                   'f1_score', 'fbeta_score',
                   'precision_score', 'recall_score']
        regressors = ['ard']
        reg_met = ['mse', 'mae', 'rmse', 'msle', 'r2', 'mape', 'smape']

        predefined_functions = classifiers + regressors
        predefined_metrics = clf_met + reg_met

        if isinstance(objective, str):
            if objective in predefined_functions:
                # logger.info(f"Found only one objective function to optimize.")
                pass
            else:
                logger.error(
                    f"Provided objective function not supported. Provided{objective}")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_functions}"
                )
        elif isinstance(objective, List):
            if set(objective).issubset(set(predefined_functions)):
                # logger.info(f"Multiple objective functions found.")
                pass
            else:
                logger.error(
                    f"One or more objective functions provided, are not supported. Provided:\n{objective}")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_functions}"
                )

        if isinstance(metrics, str):
            logger.info(f"{metrics}")
            if metrics in predefined_metrics:
                logger.info(f"Found only one metrics to optimize: {metrics}")
                pass
            else:
                logger.error(f"Provided metrics not supported. Provided: {metrics}")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_metrics}"
                )
        elif isinstance(metrics, List):
            if set(metrics).issubset(set(predefined_metrics)):
                # logger.info(f"Multiple metrics found.")
                pass
            else:
                logger.error(
                    f"One or more metrics provided, are not supported. Provided:\n{metrics}")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_metrics}"
                )

    # Instance checker
    @staticmethod
    def verify_input_types(objective: Union[str, List], metrics: Union[str, List]) -> None:
        """
        Verifying whether the given inputs are of the
        correct type

        Parameters
        ----------
        objective: Union[str, List]
            objective functions to check
        metrics: Union[str, List]
            metrics to check

        Returns
        -------
        None
        """
        if isinstance(objective, str):
            logger.info(
                f"Found only one objective function to optimize.")
        elif objective is None:
            logger.warning(f"Considering all default objective functions for calculations.")
        elif isinstance(objective, List):
            if all(isinstance(obj, str) for obj in objective):
                pass
            else:
                logger.error(
                    f"Currently the parameter `objective` only supports str or List[str].")
                raise TypeError(
                    f"One or more elements of your list has an invalid type."
                )
        else:
            logger.error(
                f"Currently the parameter `objective` only supports str or List[str].")
            raise TypeError(
                f"You passed in {type(objective)}"
            )

        if isinstance(metrics, str):
            logger.info(f"Found only one metric to optimize.")
        elif isinstance(metrics, List):
            if all(isinstance(met, str) for met in metrics):
                pass
            else:
                logger.error(
                    f"Currently the parameter `metrics` only supports str or List[str].")
                raise TypeError(
                    f"One or more elements of your list has an invalid type."
                )
        else:
            logger.error(
                f"Currently the parameter `metrics` only supports str or List[str].")
            raise TypeError(
                f"You passed in {type(metrics)}"
            )

    # Checking integrity of the inputs
    def integrity_check(self, objective: Union[str, List],
                        metrics: Union[str, List]) -> Tuple[Union[str, List[str]], Union[str, List[str]]]:
        """
        Checking the integrity of the inputs.
        Specifically, objective and metrics.

        Parameters
        ----------
        objective: Union[str, List]
            objective functions to check
        metrics: Union[str, List]
            metrics to check

        Returns
        -------
        tuple: Tuple[Union[str, List[str]],
                    Union[str, List[str]]]
            a tuple of clean objective functions and
            metrics
        """
        logger.info(f"PERFORMING INPUT INTEGRITY CHECK...")
        self.verify_input_types(objective, metrics)
        self.verify_input(objective, metrics)
        new_objective, new_metrics = objective, metrics
        if isinstance(objective, List):
            new_objective = list(set(objective))
            if len(new_objective) != len(objective):
                logger.warning(
                    f"Duplicated objective functions found. Each function will only be calculated once.")
            if len(new_objective) == 1:
                new_objective = new_objective[0]
                logger.warning(f"Multiple objectives passed in but only one unique objective found.")
            else:
                logger.info(f"Found multiple objective functions. Tuning might take a while.")

        if isinstance(metrics, List):
            new_metrics = list(set(metrics))
            if len(new_metrics) != len(metrics):
                logger.warning(
                    f"Duplicated metrics found. Each metric will only be calculated once.")
            if len(new_metrics) == 1:
                new_metrics = new_metrics[0]
            else:
                logger.warning(f"Found multiple metrics to optimize.")

        logger.info(f"INTEGRITY CHECK SUCCESSFUL...")

        return new_objective, new_metrics


# class ClassificationTuner
class ClassificationTuner(BaseTuner):
    """
                Tuning parameters for predefined
                classifiers  using
                `OPTUNA
                <https://github.com/optuna/optuna>`_.
                For a detailed example on how to use
                ClassificationTuner, check `this
                <__init__.py>`_ out.

                Parameters
                ----------
                x: Union[pd.DataFrame, pd.Series]
                    input data
                y: Union[pd.DataFrame, pd.Series]
                    target data
                objective: Union[str, List[str]]
                    objective function to tune the
                    parameters for. Default: 'rf'
                save_loc: Union[str, Path]
                    location to save the end results
                metrics: Union[str, List[str]]
                    metrics to optimize for the objective.
                    Default: 'roc_auc_score'
                metrics_directions: Union[str, List[str]]
                    direction(s) to optimize the metrics.
                    Default: 'maximize'
                cv: Union[int, Any]
                    either an integer for StratifiedKFold
                    or StratifiedGroupKFold or any
                    cv method that has split(X,y,groups)
                    Default: 5
                group_col: str
                    name of the group column in case of
                    StratifiedGroupKFold or similar
                random_state: int
                    random initializing state for
                    reproducibility. Default: 42
                params: dict
                    A fixed value for the  hyperparameters
                    of the objective function

                Methods
                -------
                tune_classifier( optimization_config: Dict | None,
                max_trials_callback: int)
                    takes in the configuration for
                    study.optimize(objective,
                    optimization_config) and tunes the
                    objective function.
                    `optimization_config` must be a Dict
                    and the allowed parameters can be
                    found `here
                    <https://optuna.readthedocs.io/en/
                    stable/reference/generated/optuna.
                    study.Study.html#
                    optuna.study.Study.optimize>`_

                Raises
                ------
                ValueError
                    Raised when length of `metrics`
                    do not match the length of
                     `metrics_directions`
                TypeError
                    Raised when either objective or
                    metrics contains an unsupported type

                See Also
                --------
                RegressionTuner: Tuner for regression
                    problems `<RegressionTuner>`_

                Notes
                -----
                In progres...

                Examples
                --------
                >>> objective = 'lr'
                >>> metrics = 'roc_auc_score'
                >>> direction = 'maximize'
                >>> cv = KFold(n_splits=3,
                                         shuffle=True,
                                         random_state=99)
                >>> optimization_config = {
                            'n_trials': 5,
                            'timeout': 3600
                        }
                >>> max_trials_callback = 5
                >>> params = {
                            'max_iter': 500
                        }
                >>> x = pd.DataFrame() # your df
                >>> y = pd.DataFrame() # your target
                >>> tuner = ClassificationTuner(x, y,
                                                                 objective,
                                                                 'tmp/data',
                                                                 metrics,
                                                                 direction,
                                                                 cv,
                                                                 42,
                                                                 params)
                >>> tuner.tune_classifier(optimization_config,
                                        max_trials_callback)
                """

    def __init__(self, x: Union[pd.DataFrame, pd.Series],
                 y: Union[pd.DataFrame, pd.Series],
                 save_loc: Union[str, Path],
                 objective: Union[str, List] = 'rf',
                 metrics: Union[str, List] = 'roc_auc_score',
                 metrics_directions: Union[str, List] = 'maximize',
                 cv: Union[int, Any] = 5, group_col: str = None,
                 random_state: int = 42, params: dict = None):
        super().__init__(x, y, save_loc, cv, group_col, random_state)
        self.objectives, self.metrics = self.integrity_check(objective,
                                                             metrics)
        self.obj_params = params
        logger.info(f"Objective functions: {self.objectives}")
        logger.info(f"Metrics: {self.metrics}")
        self.directions = metrics_directions
        if isinstance(self.directions, List):
            # noinspection PyTypeChecker
            if len(metrics_directions) != len(self.metrics):
                logger.error(
                    f"Length missmatch. If you provided the same lengths for `metrics` and `metrics_directions`,"
                    f"check if there are duplicates in `metrics`. Duplicates are removed as a part of integrity check."
                    f"Hence, it can lead to a length missmatch.")
                raise ValueError(
                    f"`metrics` and `metrics_directions` must have the same length."
                )

    # Tuner
    # noinspection PyTypeChecker
    def tune_classifier(self, optimization_config: Dict = None,
                        max_trials_callback: int = 1000):
        """
            Tuning the classifiers

            Parameters
            ----------
            optimization_config: Dict | None
                Configuration parameters for optuna.
                study.Study.optimize. Default: None
                i.e. optimization_config = {
                    'n_trials': 1000,
                    'timeout': 3600
                    }
            max_trials_callback: int
                When running multiple studies, this will
                be the total number of trials for all
                the studies combined. Default: 1000

            Returns
            -------
            None
            """
        self.load_objective_functions()
        self.tune(optimization_config, max_trials_callback,
                  self.directions, self.metrics)

    # Importing the objective functions from objective scripts and passing them on to the _tune
    def load_objective_functions(self):
        """
        Mapping user keywords for objectives with
        predefined objective functions. Class
        attribute objective_fn is updated accordingly

        Returns
        -------
        None
        """
        function_map = {
            'lr': self.lr_objective,
            'svm': self.svm_objective,
            'xgb': self.xgb_objective,
            'rf': self.rf_objective,
            'dt': self.dt_objective,
            'cat': self.cat_objective,
            'lgbm': self.lgbm_objective,
            'sgd': self.sgd_objective,
            'ridge': self.ridge_objective,
            'gnb': self.gnb_objective
        }
        if isinstance(self.objectives, str):
            self.objective_fn = function_map[self.objectives]
        else:
            self.objective_fn = []
            for obj in self.objectives:
                self.objective_fn.append(function_map[obj])

    # Method to calculate the specified score
    def calculate_metrics(self, estimator: Any,
                          x: Union[pd.DataFrame, pd.Series, np.ndarray],
                          y: Union[
                              pd.DataFrame, pd.Series, np.ndarray]) -> \
            Union[float, List[float]]:
        """
        Calculating score(s) / loss(es) and returning
        what the user asked for with a trained
        estimator, input data, and ground truth.

        Parameters
        ----------
        estimator: Any
            a trained or fitted estimator
        x: Union[pd.DataFrame, pd.Series,
                np.ndarray]
            input_data
        y: Union[pd.DataFrame, pd.Series,
                np.ndarray]
            target data

        Returns
        -------
        metrics: Union[float, List[float]]
            score(s) / loss(es) specified by the user
        """
        roc_auc, accuracy, f1, fbeta, precision, recall, jaccard, logloss, cm = Scorer.classification_scores(
            estimator=estimator, x=x, y=y
        )
        # Metrics mapping
        metrics_map = {
            'roc_auc_score': roc_auc,
            'accuracy_score': accuracy,
            'f1_score': f1,
            'fbeta_score': fbeta,
            'precision_score': precision,
            'recall_score': recall,
            'jaccard_score': jaccard,
            'log_loss': logloss,
        }
        if isinstance(self.metrics, str):
            return metrics_map[self.metrics]
        return [metrics_map[m] for m in self.metrics]

    # LogisticRegression
    def lr_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for LogisticRegression

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'max_iter': trial.suggest_int('max_iter', 100, 1000),
            'penalty': trial.suggest_categorical('penalty', ['l1', 'l2',
                                                             'elasticnet']),
            'C': trial.suggest_float('C', 0.1, 5.0)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)

        # Selecting 'SOLVER' parameter based on labels and penalties
        if 'solver' not in params:
            if params['penalty'] == 'l1':
                params['solver'] = random.choice(['liblinear', 'saga'])
            elif params['penalty'] == 'l2':
                if self.unique_length > 2:
                    params['solver'] = random.choice(
                        ['newton-cg', 'sag', 'saga', 'lbfgs'])
                else:
                    params['solver'] = random.choice(
                        ['newton-cg', 'sag', 'saga', 'lbfgs', 'liblinear'])
            else:
                params['solver'] = 'saga'

        # Specifying 'L1_Ratio' parameter only if 'ELASTICNET' is used as penalty
        if 'l1_ratio' not in params:
            if params['penalty'] == 'elasticnet':
                params['l1_ratio'] = trial.suggest_float('l1_ratio', 0.1,
                                                         0.9)

        # Classifier
        lr = LogisticRegression(**params)
        scores = self.get_scores(estimator=lr, metric_func=self.calculate_metrics)
        self.params.append(lr.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # SVMClassifier
    def svm_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for SupportVectorMachine
        - SVC classifier.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'kernel': trial.suggest_categorical('kernel',
                                                ['linear', 'poly',
                                                 'rbf', 'sigmoid']),
            'probability': True,
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)

        # Selecting degree
        if 'degree' not in params:
            if params['kernel'] == 'poly':
                params['degree'] = trial.suggest_int('degree', 2, 7)
        # Selecting gamma
        if 'gamma' not in params:
            if params['kernel'] in ['rbf', 'poly', 'sigmoid']:
                params['gamma'] = random.choice(['scale', 'auto'])
            else:
                params['gamma'] = 'auto'
        # coef0
        if 'coef0' not in params:
            if params['kernel'] in ['poly', 'sigmoid']:
                params['coef0'] = trial.suggest_float('coef0', 0.0, 1.0)

        # Classifier
        svc = SVC(**params)
        scores = self.get_scores(estimator=svc, metric_func=self.calculate_metrics)
        self.params.append(svc.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # XGBoost
    def xgb_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for XGBoost.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'use_label_encoder': False,
            'random_state': self.random_state,
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000, 50),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 0.1),
            'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Enabling 'gpu_hist' if 'CUDA' is available
        if 'tree_method' not in params:
            if self.cuda_build:
                params['tree_method'] = trial.suggest_categorical(
                    'tree_method', ['approx', 'gpu_hist'])
            else:
                params['tree_method'] = trial.suggest_categorical(
                    'tree_method', ['approx', 'hist'])
        # Checking for categorical columns and finding minimum number of categories to onehot and maximum
        cat_cols = self.x.select_dtypes('category').columns.tolist()
        if len(cat_cols) >= 1:
            max_ohc = sum([self.x[c].nunique() for c in cat_cols])
            min_ohc = min(10, min([self.x[c].nunique() for c in cat_cols]))
            params['enable_categorical'] = True
            params['max_cat_to_onehot'] = trial.suggest_int('max_cat_to_onehot',
                                                            min_ohc, max_ohc)

            logger.warning(f"Found categorical_columns:\n{cat_cols}")
            logger.warning(
                f"Enabling OneHotEncoding with different number of one hot features."
                f"Minimum {min_ohc} features, Maximum {max_ohc}")

        # Classifier
        xgb = XGBClassifier(**params)
        scores = self.get_scores(estimator=xgb, metric_func=self.calculate_metrics)
        self.params.append(xgb.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # RandomForest
    def rf_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for RandomForest

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000, 50),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy', 'log_loss']),
            'min_samples_split': trial.suggest_float('min_samples_split', 0.0, 0.3),
            'min_samples_leaf': trial.suggest_float('min_samples_leaf', 0.0, 0.15),
            'max_features': trial.suggest_categorical('max_features',
                                                      ['sqrt', 'log2']),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
            'class_weight': 'balanced',
            'ccp_alpha': trial.suggest_float('ccp_alpha', 1e-3, 0.5)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # OutOfBag sample
        if params['bootstrap']:
            if 'oob_score' not in params:
                params['oob_score'] = True
            if 'class_weight' not in params:
                params['class_weight'] = 'balanced_subsample'
            if 'max_samples' not in params:
                params['max_samples'] = 0.85

        # Classifier
        rf = RandomForestClassifier(**params)
        scores = self.get_scores(estimator=rf, metric_func=self.calculate_metrics)
        self.params.append(rf.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # DecisionTrees
    def dt_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for DecisionTrees.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'criterion': trial.suggest_categorical('criterion',
                                                   ['gini', 'entropy',
                                                    'log_loss']),
            'splitter': trial.suggest_categorical('splitter',
                                                  ['best', 'random']),
            'min_samples_split': trial.suggest_float(
                'min_samples_split', 0.0, 0.3),
            'min_samples_leaf': trial.suggest_float('min_samples_leaf',
                                                    0.0, 0.15),
            'max_features': trial.suggest_categorical('max_features',
                                                      ['sqrt', 'log2']),
            'class_weight': 'balanced',
            'ccp_alpha': trial.suggest_float('ccp_alpha', 1e-3, 0.5),
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Classifier
        dt = DecisionTreeClassifier(**params)
        scores = self.get_scores(estimator=dt, metric_func=self.calculate_metrics)
        self.params.append(dt.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # CatBoost
    def cat_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for CATBoost.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'verbose': False,
            'random_seed': self.random_state,
            'iterations': trial.suggest_int('n_estimators', 100, 1000,
                                            step=50),
            'learning_rate': trial.suggest_float('learning_rate', 0.01,
                                                 1.),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 0.1, 10.),
            'use_best_model': False,
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'grow_policy': trial.suggest_categorical('grow_policy',
                                                     ['SymmetricTree',
                                                      'Depthwise',
                                                      'Lossguide'])
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Checking for categorical columns and finding minimum number of categories to onehot and maximum
        cat_cols = self.x.select_dtypes('category').columns.tolist()
        if len(cat_cols) >= 1:
            max_ohc = sum([self.x[c].nunique() for c in cat_cols])
            min_ohc = min(10,
                          min([self.x[c].nunique() for c in cat_cols]))
            params['cat_features'] = np.array(cat_cols)
            params['one_hot_max_size'] = trial.suggest_int(
                'max_cat_to_onehot', min_ohc, max_ohc)

            logger.warning(f"Found categorical_columns:\n{cat_cols}")
            logger.warning(
                f"Enabling OneHotEncoding with different number of one hot features."
                f"Minimum {min_ohc} features, Maximum {max_ohc}")
        # Score-Function
        if 'score_function' not in params:
            if self.cuda_build:
                if params['grow_policy'] == 'Lossguide':
                    params['score_function'] = random.choice(
                        ['L2', 'NewtonL2'])
                else:
                    params['score_function'] = random.choice(
                        ['Cosine', 'L2', 'NewtonL2', 'NewtonCosine'])
            else:
                if params['grow_policy'] == 'Lossguide':
                    params['score_function'] = 'L2'
                else:
                    params['score_function'] = random.choice(
                        ['Cosine', 'L2'])
        # Classifier
        cat = CatBoostClassifier(**params)
        scores = self.get_scores(estimator=cat, metric_func=self.calculate_metrics)
        self.params.append(cat.get_all_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # LightGBM
    def lgbm_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for LightGBM.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'importance_type': 'gain',
            'boosting_type': trial.suggest_categorical('boosting_type',
                                                       ['rf', 'gbdt',
                                                        'dart',
                                                        'goss']),
            'num_leaves': trial.suggest_int('num_leaves', 2, 100, 2),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5,
                                                 0.1),
            'n_estimators': trial.suggest_int('n_estimators', 100,
                                              1000),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        if 'subsample' not in params:
            if params['boosting_type'] != 'goss':
                params['subsample'] = 0.9
                params['subsample_freq'] = int(params['n_estimators'] / 2)

        # Checking if target is balanced
        unique_labels = self.y.unique()
        value_counts = self.y.value_counts()
        ratio = 1 / len(unique_labels)
        ratio_orig = [i / sum(value_counts) for i in value_counts]
        balanced = all([ratio - 0.05 < ro < ratio + 0.05 for ro in ratio_orig])
        if balanced:
            params['is_unbalanced'] = False
        else:
            params['is_unbalanced'] = True

        # Classifier
        lgbm = LGBMClassifier(**params)
        scores = self.get_scores(estimator=lgbm, metric_func=self.calculate_metrics)
        self.params.append(lgbm.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # SGDClassifier
    def sgd_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for SGD -
        StochasticGradientDescent

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'loss': trial.suggest_categorical('loss',
                                              ['hinge', 'log_loss',
                                               'modified_huber',
                                               'squared_hinge',
                                               'perceptron']),
            'penalty': trial.suggest_categorical('penalty', ['l1', 'l2',
                                                             'elasticnet']),
            'alpha': trial.suggest_float('alpha', 1e-3, 1),
            'learning_rate': trial.suggest_categorical('learning_rate',
                                                       ['optimal',
                                                        'adaptive',
                                                        'constant',
                                                        'invscaling']),
            'early_stopping': True
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # ETA0 and POWER_T
        if 'eta0' not in params:
            if params['learning_rate'] == 'constant':
                params['eta0'] = 0.01
            else:
                params['eta0'] = 0.1
        if 'power_t' not in params:
            if params['learning_rate'] == 'invscaling':
                params['power_t'] = trial.suggest_float('power_t', -1.0,
                                                        1.0)

        # Classifier
        sgd = SGDClassifier(**params)
        scores = self.get_scores(estimator=sgd, metric_func=self.calculate_metrics)
        self.params.append(sgd.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # RidgeClassifier
    def ridge_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for RidgeClassifier.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'alpha': trial.suggest_float('alpha', 0.01, 1),
            'solver': trial.suggest_categorical('solver',
                                                ['auto', 'svd',
                                                 'cholesky', 'lsqr',
                                                 'sparse_cg', 'sag',
                                                 'saga', 'lbfgs']),
            'class_weight': 'balanced'
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Positive coefficients
        if 'positive' not in params:
            if params['solver'] == 'lbfgs':
                params['positive'] = True

        # Classifier
        ridge = RidgeClassifier(**params)
        scores = self.get_scores(estimator=ridge, metric_func=self.calculate_metrics)
        self.params.append(ridge.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # GaussianNB
    def gnb_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for GaussianNB.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'var_smoothing': trial.suggest_float('var_smoothing', 1e-10,
                                                 0.1, )
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Classifier
        gnb = GaussianNB(**params)
        scores = self.get_scores(estimator=gnb, metric_func=self.calculate_metrics)
        self.params.append(gnb.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score


# class RegressionTuner
class RegressionTuner(BaseTuner):
    """
                Tuning parameters for predefined
                classifiers  using
                `OPTUNA
                <https://github.com/optuna/optuna>`_.
                For a detailed example on how to use
                RegressionTuner, check `this
                <__init__.py>`_ out.

                Parameters
                ----------
                x: Union[pd.DataFrame, pd.Series]
                    input data
                y: Union[pd.DataFrame, pd.Series]
                    target data
                objective: Union[str, List[str]]
                    objective function to tune the
                    parameters for. Default: 'lr'
                save_loc: Union[str, Path]
                    location to save the end results
                metrics: Union[str, List[str]]
                    metrics to optimize for the objective.
                    Default: mse
                metrics_directions: Union[str, List[str]]
                    direction(s) to optimize the metrics.
                    Default: 'minimize
                cv: Union[int, Any]
                    either an integer for StratifiedKFold
                    or StratifiedGroupKFold or any
                    cv method that has split(X,y,groups).
                    Default: 5
                group_col: str
                    name of the group column in case of
                    StratifiedGroupKFold or similar
                random_state: int
                    random initializing state for
                    reproducibility. Default: 42
                params: dict
                    A fixed value for the  hyperparameters
                    of the objective function

                Methods
                -------
                tune_regressor(optimization_config: Dict | None,
                max_trials_callback: int)
                    takes in the configuration for
                    study.optimize(objective,
                    optimization_config) and tunes the
                    objective function.
                    `optimization_config` must be a Dict
                    and the allowed parameters can be
                    found `here
                    <https://optuna.readthedocs.io/en/
                    stable/reference/generated/optuna.
                    study.Study.html#
                    optuna.study.Study.optimize>`_

                Raises
                ------
                ValueError
                    Raised when length of `metrics`
                    do not match the length of
                     `metrics_directions`
                TypeError
                    Raised when either objective or
                    metrics contains an unsupported type

                See Also
                --------
                ClassificationTuner: Tuner for classification
                    problems `<ClassificationTuner>`_

                Notes
                -----
                In progres...

                Examples
                --------
                >>> objective = 'lr'
                >>> metrics = 'roc_auc_score'
                >>> direction = 'maximize'
                >>> cv = KFold(n_splits=3,
                                         shuffle=True,
                                         random_state=99)
                >>> optimization_config = {
                            'n_trials': 5,
                            'timeout': 3600
                        }
                >>> max_trials_callback = 5
                >>> x = pd.DataFrame() # your df
                >>> y = pd.DataFrame() # your target
                >>> tuner = RegressionTuner(x, y,
                                                             objective,
                                                             'tmp/data',
                                                             metrics,
                                                             direction,
                                                             cv,
                                                             42,
                                                             params)
                >>> tuner.tune_regressor(optimization_config,
                                        max_trials_callback)
                """

    def __init__(self, x: Union[pd.DataFrame, pd.Series],
                 y: Union[pd.DataFrame, pd.Series],
                 save_loc: Union[str, Path],
                 objective: Union[str, List] = 'lr',
                 metrics: Union[str, List] = 'mse',
                 metrics_directions: Union[str, List] = 'minimize',
                 cv: Union[int, Any] = 5, group_col: str = None,
                 random_state: int = 42, params: dict = None):
        super().__init__(x, y, save_loc, cv, group_col, random_state)
        self.objectives, self.metrics = self.integrity_check(objective,
                                                             metrics)
        self.obj_params = params
        logger.info(f"Objective functions: {self.objectives}")
        logger.info(f"Metrics: {self.metrics}")
        self.directions = metrics_directions
        if isinstance(self.directions, List):
            # noinspection PyTypeChecker
            if len(metrics_directions) != len(self.metrics):
                logger.error(
                    f"Length missmatch. If you provided the same lengths for `metrics` and `metrics_directions`,"
                    f"check if there are duplicates in `metrics`. Duplicates are removed as a part of integrity check."
                    f"Hence, it can lead to a length missmatch.")
                raise ValueError(
                    f"`metrics` and `metrics_directions` must have the same length."
                )

    # Tuner
    # noinspection PyTypeChecker
    def tune_regressor(self, optimization_config: Dict = None,
                       max_trials_callback: int = 1000):
        """
        Tuning the regressors

        Parameters
        ----------
        optimization_config: Dict | None
            Configuration parameters for optuna.
            study.Study.optimize. Default: None
            i.e. optimization_config = {
                'n_trials': 1000,
                'timeout': 3600
                }
        max_trials_callback: int
            When running multiple studies, this will
            be the total number of trials for all
            the studies combined. Default: 1000

        Returns
        -------
        None
        """
        self.load_objective_functions()
        self.tune(optimization_config, max_trials_callback,
                  self.directions, self.metrics)

    # Importing the objective functions from objective scripts and passing them on to the _tune
    def load_objective_functions(self):
        """
        Mapping user keywords for objectives with
        predefined objective functions. Class
        attribute objective_fn is updated accordingly

        Returns
        -------
        None
        """
        function_map = {
            'ard': self.ard_objective,
            'dt': self.dt_objective,
            'svm': self.svm_objective,
            'xgb': self.xgb_objective,
            'rf': self.rf_objective,
            'cat': self.cat_objective,
            'lgbm': self.lgbm_objective,
            'sgd': self.sgd_objective
        }
        if isinstance(self.objectives, str):
            self.objective_fn = function_map[self.objectives]
        else:
            self.objective_fn = []
            for obj in self.objectives:
                self.objective_fn.append(function_map[obj])

    # Method to calculate the specified score
    def calculate_metrics(self, estimator: Any,
                          x: Union[pd.DataFrame, pd.Series, np.ndarray],
                          y: Union[
                              pd.DataFrame, pd.Series, np.ndarray]) -> \
            Union[float, List[float]]:
        """
            Calculating score(s) / loss(es) and returning
            what the user asked for with a trained
            estimator, input data, and ground truth.

            Parameters
            ----------
            estimator: Any
                a trained or fitted estimator
            x: Union[pd.DataFrame, pd.Series,
                    np.ndarray]
                input_data
            y: Union[pd.DataFrame, pd.Series,
                    np.ndarray]
                target data

            Returns
            -------
            metrics: Union[float, List[float]]
                score(s) / loss(es) specified by the user
            """
        r2, max_e, mae, meae, mape, mse, msle, rmse, rmsle, smape = Scorer.regression_scores(
            estimator=estimator, x=x, y=y
        )
        # Metrics mapping
        metrics_map = {
            'mae': mae,
            'mape': mape,
            'median_ae': meae,
            'smape': smape,
            'mse': mse,
            'rmse': rmse,
            'msle': msle,
            'rmsle': rmsle,
            'r2': r2,
            'max_error': max_e,
        }
        if isinstance(self.metrics, str):
            return metrics_map[self.metrics]
        return [metrics_map[m] for m in self.metrics]

    # Automatic Relevance Determination - ARD
    def ard_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for LogisticRegression

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'n_iter': trial.suggest_int('n_iter', 100, 1000),
            'alpha_1': trial.suggest_float('alpha_1', 1e-7, 1e-1),
            'alpha_2': trial.suggest_float('alpha_2', 1e-7, 1e-1),
            'lambda_1': trial.suggest_float('lambda_1', 1e-7, 1e-1),
            'lambda_2': trial.suggest_float('lambda_2', 1e-7, 1e-1),
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Regressor
        lr = ARDRegression(**params)
        scores = self.get_scores(estimator=lr, metric_func=self.calculate_metrics)
        self.params.append(lr.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # SVMClassifier
    def svm_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for SupportVectorMachine
        - SVC classifier.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'kernel': trial.suggest_categorical('kernel',
                                                ['linear', 'poly',
                                                 'rbf', 'sigmoid']),
            'C': trial.suggest_float('C', 0.5, 10, step=0.05),
            'epsilon': trial.suggest_float('epsilon', 0.1, 0.25),
            'max_iter': trial.suggest_int('max_iter', -1, 1000, step=50)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)

        # Selecting degree
        if 'degree' not in params:
            if params['kernel'] == 'poly':
                params['degree'] = trial.suggest_int('degree', 2, 7)
        # Selecting gamma
        if 'gamma' not in params:
            if params['kernel'] in ['rbf', 'poly', 'sigmoid']:
                params['gamma'] = random.choice(['scale', 'auto'])
            else:
                params['gamma'] = 'auto'
        # coef0
        if 'coef0' not in params:
            if params['kernel'] in ['poly', 'sigmoid']:
                params['coef0'] = trial.suggest_float('coef0', 0.0, 1.0)

        # Classifier
        svc = SVR(**params)
        scores = self.get_scores(estimator=svc, metric_func=self.calculate_metrics)
        self.params.append(svc.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # XGBoost
    def xgb_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for XGBoost.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000, 50),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 0.1),
            'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1),
            'grow_policy': trial.suggest_int('grow_policy', 0, 10)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)

        # Enabling 'gpu_hist' if 'CUDA' is available
        if 'tree_method' not in params:
            if self.cuda_build:
                params['tree_method'] = trial.suggest_categorical(
                    'tree_method', ['approx', 'gpu_hist'])
            else:
                params['tree_method'] = trial.suggest_categorical(
                    'tree_method', ['approx', 'hist'])
        # Checking for categorical columns and finding minimum number of categories to onehot and maximum
        cat_cols = self.x.select_dtypes('category').columns.tolist()
        if len(cat_cols) >= 1:
            max_ohc = sum([self.x[c].nunique() for c in cat_cols])
            min_ohc = min(10, min([self.x[c].nunique() for c in cat_cols]))
            params['enable_categorical'] = True
            params['max_cat_to_onehot'] = trial.suggest_int('max_cat_to_onehot',
                                                            min_ohc, max_ohc)

            logger.warning(f"Found categorical_columns:\n{cat_cols}")
            logger.warning(
                f"Enabling OneHotEncoding with different number of one hot features."
                f"Minimum {min_ohc} features, Maximum {max_ohc}")

        # Classifier
        xgb = XGBRegressor(**params)
        scores = self.get_scores(estimator=xgb, metric_func=self.calculate_metrics)
        self.params.append(xgb.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # RandomForest
    def rf_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for RandomForest

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000, 50),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'criterion': trial.suggest_categorical('criterion', ['squared_error', 'absolute_error',
                                                                 'friedman_mse', 'poisson']),
            'min_samples_split': trial.suggest_float('min_samples_split', 0.0, 0.3),
            'min_samples_leaf': trial.suggest_float('min_samples_leaf', 0.0, 0.15),
            'max_features': trial.suggest_categorical('max_features',
                                                      ['sqrt', 'log2']),
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
            'ccp_alpha': trial.suggest_float('ccp_alpha', 1e-3, 0.5)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # OutOfBag sample
        if params['bootstrap']:
            if 'oob_score' not in params:
                params['oob_score'] = True
            if 'class_weight' not in params:
                params['class_weight'] = 'balanced_subsample'
            if 'max_samples' not in params:
                params['max_samples'] = 0.85

        # Classifier
        rf = RandomForestRegressor(**params)
        scores = self.get_scores(estimator=rf, metric_func=self.calculate_metrics)
        self.params.append(rf.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # DecisionTrees
    def dt_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for DecisionTrees.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'criterion': trial.suggest_categorical('criterion',
                                                   ['squared_error', 'friedman_mse',
                                                    'absolute_error', 'poisson']),
            'splitter': trial.suggest_categorical('splitter',
                                                  ['best', 'random']),
            'min_samples_split': trial.suggest_float(
                'min_samples_split', 0.0, 0.3),
            'min_samples_leaf': trial.suggest_float('min_samples_leaf',
                                                    0.0, 0.15),
            'max_features': trial.suggest_categorical('max_features',
                                                      ['sqrt', 'log2']),
            'ccp_alpha': trial.suggest_float('ccp_alpha', 1e-3, 0.5),
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Classifier
        dt = DecisionTreeRegressor(**params)
        scores = self.get_scores(estimator=dt, metric_func=self.calculate_metrics)
        self.params.append(dt.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # CatBoost
    def cat_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for CATBoost.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'verbose': False,
            'random_seed': self.random_state,
            'iterations': trial.suggest_int('n_estimators', 100, 1000,
                                            step=50),
            'learning_rate': trial.suggest_float('learning_rate', 0.01,
                                                 1.),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 0.1, 10.),
            'use_best_model': False,
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'grow_policy': trial.suggest_categorical('grow_policy',
                                                     ['SymmetricTree',
                                                      'Depthwise',
                                                      'Lossguide'])
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # Checking for categorical columns and finding minimum number of categories to onehot and maximum
        cat_cols = self.x.select_dtypes('category').columns.tolist()
        if len(cat_cols) >= 1:
            max_ohc = sum([self.x[c].nunique() for c in cat_cols])
            min_ohc = min(10,
                          min([self.x[c].nunique() for c in cat_cols]))
            params['cat_features'] = np.array(cat_cols)
            params['one_hot_max_size'] = trial.suggest_int(
                'max_cat_to_onehot', min_ohc, max_ohc)

            logger.warning(f"Found categorical_columns:\n{cat_cols}")
            logger.warning(
                f"Enabling OneHotEncoding with different number of one hot features."
                f"Minimum {min_ohc} features, Maximum {max_ohc}")
        # Score-Function
        if 'score_function' not in params:
            if self.cuda_build:
                if params['grow_policy'] == 'Lossguide':
                    params['score_function'] = random.choice(
                        ['L2', 'NewtonL2'])
                else:
                    params['score_function'] = random.choice(
                        ['Cosine', 'L2', 'NewtonL2', 'NewtonCosine'])
            else:
                if params['grow_policy'] == 'Lossguide':
                    params['score_function'] = 'L2'
                else:
                    params['score_function'] = random.choice(
                        ['Cosine', 'L2'])
        # Classifier
        cat = CatBoostRegressor(**params)
        scores = self.get_scores(estimator=cat, metric_func=self.calculate_metrics)
        self.params.append(cat.get_all_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # LightGBM
    def lgbm_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for LightGBM.

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'importance_type': 'gain',
            'boosting_type': trial.suggest_categorical('boosting_type',
                                                       ['rf', 'gbdt',
                                                        'dart',
                                                        'goss']),
            'num_leaves': trial.suggest_int('num_leaves', 10, 100, 2),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5,
                                                 1.0),
            'n_estimators': trial.suggest_int('n_estimators', 100,
                                              1000),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        if 'subsample' not in params:
            if params['boosting_type'] != 'goss':
                params['subsample'] = 0.9
                params['subsample_freq'] = int(params['n_estimators'] / 2)

        # Checking if target is balanced
        unique_labels = self.y.unique()
        value_counts = self.y.value_counts()
        ratio = 1 / len(unique_labels)
        ratio_orig = [i / sum(value_counts) for i in value_counts]
        balanced = all([ratio - 0.05 < ro < ratio + 0.05 for ro in ratio_orig])
        if balanced:
            params['is_unbalanced'] = False
        else:
            params['is_unbalanced'] = True

        # Classifier
        lgbm = LGBMRegressor(**params)
        scores = self.get_scores(estimator=lgbm, metric_func=self.calculate_metrics)
        self.params.append(lgbm.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # SGDClassifier
    def sgd_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for SGD -
        StochasticGradientDescent

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'loss': trial.suggest_categorical('loss',
                                              ['squared_error', 'huber',
                                               'epsilon_insensitive',
                                               'squared_epsilon_insensitive']),
            'penalty': trial.suggest_categorical('penalty', ['l1', 'l2',
                                                             'elasticnet']),
            'alpha': trial.suggest_float('alpha', 1e-5, 1),
            'learning_rate': trial.suggest_categorical('learning_rate',
                                                       ['optimal',
                                                        'adaptive',
                                                        'constant',
                                                        'invscaling']),
            'early_stopping': True
        }
        # Updating params to adjust fixed values
        if self.obj_params is not None:
            params.update(self.obj_params)
        # ETA0 and POWER_T
        if 'eta0' not in params:
            if params['learning_rate'] == 'constant':
                params['eta0'] = 0.01
            else:
                params['eta0'] = 0.1
        if 'power_t' not in params:
            if params['learning_rate'] == 'invscaling':
                params['power_t'] = trial.suggest_float('power_t', -1.0,
                                                        1.0)

        # Classifier
        sgd = SGDRegressor(**params)
        scores = self.get_scores(estimator=sgd, metric_func=self.calculate_metrics)
        self.params.append(sgd.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score


# class ParamsLoader
class ParamsLoader:
    """
                    Loading the parameters from a csv
                    file generated by `ClassificationTuner
                    <ClassificationTuner>`_ or `RegressionTuner
                    <RegressionTuner>`_

                    Parameters
                    ----------
                    params_csv: Union[str, List]
                        path to params.csv file
                    column_name: str
                        this parameter checks the
                        `fetch` argument and
                        extracts the maximum from this
                        column
                    index_id: int
                        if column_name is none, it will
                        use index id. Usefull when you
                        have multiple metrics and want to
                        do a trade-off
                    save_loc: Union[str, Path]
                        location to save the params.
                        If None, file will not be saved.
                    fetch: str
                        fetching max, min,  mean, median, or mode
                         value in the `column_name`
                         column. When used with
                        `index_id`, this parameter has no
                        effect.

                    Methods
                    -------
                    load_params()
                        loads only the non-null parameters
                        from the csv file and returns a
                        dictionary

                    Raises
                    ------
                    AttributeError
                        Raised when both `column_name`
                        and `index_id` are provided at the
                        same time

                    See Also
                    --------
                    ClassificationTuner: `<ClassificationTuner>`_
                    RegressionTuner: `<RegressionTuner>`_

                    Examples
                    --------
                    >>> pl = ParamsLoader('params.csv',
                                                    'col1',
                                                    save_loc='.',
                                                    fetch='max')
                    >>> params = pl.load_params()
                    """

    # noinspection PyTypeChecker
    def __init__(self, params_csv: Union[str, Path], column_name: str = None,
                 index_id: int = None, save_loc: Union[str, Path] = None,
                 fetch: str = 'max'):
        if column_name is not None and index_id is not None:
            logger.error(f"Invalid input.")
            raise AttributeError(
                f"`column_name` and `index_id` cannot be provided at the same time"
            )
        self.df = pd.read_csv(params_csv)
        self.column_name = column_name
        self.index_id = index_id
        self.save_loc = save_loc
        self.fetch = fetch
        self.cols_to_extract = [c for c in self.df.columns if c.startswith('params_')]

    # Loading the params given a column name
    # noinspection PyTypeChecker
    def load_via_column(self) -> Dict:
        """
        Loading params given a column name.

        Returns
        -------
        parameters: Dict
            non-null parameters as a dictionary
        """
        if self.fetch == 'max':
            value = max(self.df[self.column_name])
        elif self.fetch == 'min':
            value = max(self.df[self.column_name])
        elif self.fetch == 'mean':
            mean = np.nanmean(self.df[self.column_name])
            value = self.helper(mean)
        else:
            median = np.nanmedian(self.df[self.column_name])
            value = self.helper(median)

        logger.info(f"Selected params with {self.column_name}: {value}")
        params = self.df[self.df[self.column_name] == value]
        params = params[self.cols_to_extract]
        params.dropna(axis=1, inplace=True)
        new_cols = [c.replace('params_', '') for c in params.columns]
        params.columns = new_cols
        params.reset_index(inplace=True, drop=True)
        params = params.loc[0].to_dict()
        return params

    # Helper function to find out which value is nearer to a given threshold
    def helper(self, threshold: float):
        """
        Finds the nearest value to a given threshold
        Parameters
        ----------
        threshold: float
            threshold value to look for

        Returns
        -------
        value: float
            the value closest to the given threshold
        """
        v = {}
        for _, row in self.df.iterrows():
            value = row[self.column_name]
            diff = np.abs(threshold - value)
            v[value] = diff

        minimum_diff = min(v.values())
        v = {a: b for (b, a) in v.items()}
        value = v[minimum_diff]
        return value

    # Loading the params given an index
    def load_via_index(self) -> Dict:
        """
        Loading params given an index id.

        Returns
        -------
        parameters: Dict
            non-null parameters as a dictionary
        """
        params = self.df[self.cols_to_extract]
        new_cols = [c.replace('params_', '') for c in params.columns]
        params.columns = new_cols
        params = params.loc[self.index_id]
        params.dropna(inplace=True)
        params = params.to_dict()
        logger.info(f"Selected params with index: {self.index_id}"
                    f"\n{self.df.loc[self.index_id].dropna(inplace=False)}")
        return params

    # Loading and saving the params
    def load_params(self):
        """
        User function for loading the params.

        Returns
        -------
        parameters: Dict
            non-null parameters as a dictionary
        """
        if self.column_name is None:
            params = self.load_via_index()
        else:
            params = self.load_via_column()

        if self.save_loc is not None:
            # noinspection PyTypeChecker
            Path(self.save_loc).mkdir(parents=True, exist_ok=True)
            with open(f"{self.save_loc}/params.pkl", 'wb') as pf:
                pickle.dump(params, pf)

        return params
