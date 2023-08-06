"""
A script containing utility functions for ML tasks
"""
# Imports
import pandas as pd
import numpy as np
from typing import Any
from pathlib import Path
from math import sqrt
from sklearn.model_selection import train_test_split, ShuffleSplit, GroupShuffleSplit, \
    StratifiedShuffleSplit, StratifiedKFold, KFold, StratifiedGroupKFold, RepeatedKFold, \
    RepeatedStratifiedKFold, GroupKFold, LeavePGroupsOut, LeavePOut, LeaveOneOut, \
    LeaveOneGroupOut
from sklearn.metrics import roc_auc_score, accuracy_score, jaccard_score, precision_score, \
    recall_score, confusion_matrix, f1_score, fbeta_score, log_loss, r2_score, max_error, \
    mean_squared_error, mean_absolute_error, mean_squared_log_error, median_absolute_error, \
    mean_absolute_percentage_error
import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter('%(log_color)s[%(levelname).1s %(log_color)s%(asctime)s] - %(log_color)s%(name)s - '
                             '%(reset)s%(message)s')
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

"""
Author: vickyparmar
File: ml_utils.py
Created on: 10-03-2023, Fri, 15:07:20

Last modified by: vickyparmar
Last modified on: 10-3-2023, Fri, 16:18:06
"""


# Class Scorer
class Scorer:
    @staticmethod
    def classification_scores(estimator: Any,
                              x: pd.DataFrame or pd.Series or np.ndarray,
                              y: pd.DataFrame or pd.Series or np.ndarray) -> tuple:
        """
            Computes various classification evaluation metrics for the input estimator and returns them as a tuple.

            Parameters
            ----------
            estimator : Any
                A fitted classification estimator object with a `predict` method.
            x : pandas.DataFrame or pandas.Series or numpy.ndarray
                The feature matrix or vector for the input data.
            y : pandas.DataFrame or pandas.Series or numpy.ndarray
                The target vector or matrix for the input data.

            Returns
            -------
            tuple
                A tuple containing the following classification evaluation metrics:
                - roc_auc: float
                    The area under the Receiver Operating Characteristic (ROC) curve.
                - accuracy: float
                    The fraction of correctly classified samples.
                - f1: float
                    The harmonic mean of precision and recall.
                - fbeta: float
                    The weighted harmonic mean of precision and recall with weight on precision given by beta.
                - precision: float
                    The fraction of correctly classified positive samples out of all samples classified as positive.
                - recall: float
                    The fraction of correctly classified positive samples out of all positive samples.
                - jaccard: float
                    The Intersection over Union (IoU) of the predicted and true positive samples.
                - logloss: float
                    The logarithmic loss.
                - cm: numpy.ndarray
                    The confusion matrix with true labels as rows and predicted labels as columns.
            """
        predictions = estimator.predict(x)
        # Scores
        # noinspection PyBroadException
        try:
            probabilities = estimator.predict_proba(x)
            roc_auc = roc_auc_score(y_true=y, y_score=probabilities[:, 1])
        except Exception as e:
            roc_auc = np.nan
        accuracy = accuracy_score(y_true=y, y_pred=predictions)
        f1 = f1_score(y_true=y, y_pred=predictions)
        fbeta = fbeta_score(y_true=y, y_pred=predictions, beta=0.5)
        precision = precision_score(y_true=y, y_pred=predictions)
        recall = recall_score(y_true=y, y_pred=predictions)
        jaccard = jaccard_score(y_true=y, y_pred=predictions)
        logloss = log_loss(y_true=y, y_pred=predictions)
        cm = confusion_matrix(y_true=y, y_pred=predictions)

        return roc_auc, accuracy, f1, fbeta, precision, recall, jaccard, logloss, cm

    @staticmethod
    def regression_scores(estimator: Any,
                          x: pd.DataFrame or pd.Series or np.ndarray,
                          y: pd.DataFrame or pd.Series or np.ndarray) -> tuple:
        """
            Calculate various regression performance metrics.

            Parameters
            ----------
            estimator : Any
                A trained regression estimator.
            x : pd.DataFrame or pd.Series or np.ndarray
                Feature matrix.
            y : pd.DataFrame or pd.Series or np.ndarray
                Target variable.

            Returns
            -------
            tuple
                A tuple containing the following regression performance metrics:
                - r2 : float
                    R^2 (coefficient of determination) regression score function.
                - max_e : float
                    Maximum residual error.
                - mae : float
                    Mean absolute error regression loss.
                - meae : float
                    Median absolute error regression loss.
                - mape : float
                    Mean absolute percentage error regression loss.
                - mse : float
                    Mean squared error regression loss.
                - msle : float
                    Mean squared logarithmic error regression loss.
                - rmse : float
                    Root mean squared error regression loss.
                - rmsle : float
                    Root mean squared logarithmic error regression loss.
                - smape: float
                    Symmetric mean absolute percentage error.
        """
        predictions = estimator.predict(x)
        r2 = r2_score(y_true=y, y_pred=predictions)
        max_e = max_error(y_true=y, y_pred=predictions)
        mse = mean_squared_error(y_true=y, y_pred=predictions)
        mae = mean_absolute_error(y_true=y, y_pred=predictions)
        msle = mean_squared_log_error(y_true=y, y_pred=predictions)
        meae = median_absolute_error(y_true=y, y_pred=predictions)
        mape = mean_absolute_percentage_error(y_true=y, y_pred=predictions)
        rmse = sqrt(mse)
        rmsle = sqrt(msle)
        smape = round(np.mean(np.abs(y - predictions) / ((np.abs(y) + np.abs(predictions)) / 2)) * 100, 2)

        return r2, max_e, mae, meae, mape, mse, msle, rmse, rmsle, smape


# Class DataPrep
class DataPrep:
    pass
