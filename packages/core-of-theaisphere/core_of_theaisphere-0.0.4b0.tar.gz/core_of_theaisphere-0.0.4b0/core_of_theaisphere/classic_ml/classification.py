"""
This script contains classical machine learning models for classification purposes.
"""

# Imports
import pandas as pd
import numpy as np
import logging
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from ..visualizations.visualize import ClassicMLPlots

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

"""
Author: vickyparmar
File: classification.py
Created on: 07-10-2022, Fri, 1:49:04

Last modified by: vickyparmar
Last modified on: 10-10-2022, Mon, 12:15:28
"""


# [ ] ToDo: LogisticRegression
# [ ] ToDo: SVM Classifier
# [ ] ToDo: XGBoost
# [ ] ToDo: RandomForest
# [ ] ToDo: DecisionTrees
# [ ] ToDo: CatBoost
# [ ] ToDo: LightGBM
# [ ] ToDo: *NB
# [ ] ToDo: KNN and DBSCAN clustering



