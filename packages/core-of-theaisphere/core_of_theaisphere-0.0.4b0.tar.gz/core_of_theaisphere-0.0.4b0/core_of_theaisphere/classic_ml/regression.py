"""
This script contains classical machine learning models for regression purposes.
"""

# Imports
import pandas as pd
import numpy as np
import logging
from xgboost import XGBClassifier
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR, NuSVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

"""
Author: vickyparmar
File: regression.py
Created on: 04-04-2023, Tue, 18:04:05

Last modified by: vickyparmar
Last modified on: 04-4-2023, Tue, 18:04:07
"""


# [ ] ToDo: LinearRegression
# [ ] ToDo: SVR, NuSVR
# [ ] ToDo: XGBoost
# [ ] ToDo: RandomForest
# [ ] ToDo: DecisionTrees
# [ ] ToDo: CatBoost
# [ ] ToDo: LightGBM
