import numpy as np 
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import xgboost as xgb
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression, SGDClassifier, RidgeClassifier, LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, ARDRegression, SGDRegressor, PassiveAggressiveRegressor, Perceptron
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier, RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from tqdm import tqdm

from simplysklearn.metrics import *
from simplysklearn.plot import *


class Regression:
    def __init__(self, data, FeatureList, Target, EnsembleBoolean=True, NeuralBoolean=True, SplitRatio=0.3, Randomstate=42):
        # Any possible parameters 
        self.OutputType = 'regression'
        self.FeatureList = FeatureList

        if len(self.FeatureList) <= 0:
            raise Exception("There should be 1 or more features")

        self.Target = Target
        if self.Target not in data.columns.tolist():
            raise Exception("The target variable is not in the DataFrame")

        self.EnsembleBoolean = EnsembleBoolean
        if not type(self.EnsembleBoolean) is bool:
            raise TypeError("Only Boolean variables accepted for Ensemble Boolean parameter")

        self.NeuralBoolean = NeuralBoolean   
        if not type(self.NeuralBoolean) is bool:
            raise TypeError("Only Boolean variables accepted for Neural Boolean parameter")

        self.df = data # In a pandas DataFrame
        self.SplitRatio = SplitRatio
        if self.SplitRatio > 1 or self.SplitRatio < 0:
            raise Exception("Split Ratio should be between 0 and 1")

        self.RandomState = Randomstate
        self.PredictedVal = {}
        self.Scores = {}
        self.outlier_values = {}

        self.Regression_Models = [['Linear Regression', LinearRegression()], ['Ridge', Ridge()], ['Lasso', Lasso()], ['ElasticNet', ElasticNet()], 
        ['Bayesian Ridge', BayesianRidge()], ['ARDRegression', ARDRegression()], ['SGDRegressor', SGDRegressor()], 
        ['Passive Aggressive Regressor', PassiveAggressiveRegressor()], ['Perceptron', Perceptron()], ['SVR', svm.SVR()], ['Gaussian Process Regressor', GaussianProcessRegressor()], 
        ['Decision Tree Regressor', DecisionTreeRegressor()]]
        self.Ensemble_Regression_Models = [['Random Forest Regressor', RandomForestRegressor()], ['Ada Boost Regressor', AdaBoostRegressor()],
        ['Gradient Boosting Regressor', GradientBoostingRegressor()], ['XGBRegressor', xgb.XGBRegressor()]]
        self.Neural_Regression_Models = [['MLP Regressor', MLPRegressor()]]

    def __prepare_data(self, numerical_method = StandardScaler(), categorical_method = OneHotEncoder(handle_unknown='ignore', sparse_output=False)): # Private Method 
        df = self.df[self.FeatureList].copy()

        numerical_df = df.select_dtypes(include=['int', 'float'])
        categorical_df = df.select_dtypes(exclude = ['int', 'float']) # Contains object, boolean

        num_pipe = make_pipeline(
            SimpleImputer(strategy='median'),
            numerical_method
        )
        # pipeline for categorical columns
        cat_pipe = make_pipeline(
            SimpleImputer(strategy='constant', fill_value='N/A'),
            categorical_method
        )

        # combine both the pipelines
        full_pipe = ColumnTransformer([
            ('num', num_pipe, numerical_df.columns.tolist()),
            ('cat', cat_pipe, categorical_df.columns.tolist())
        ])

        return full_pipe

    def __split(self):
        X = self.df[self.FeatureList].copy()
        y = self.df[self.Target].copy()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.SplitRatio, random_state=self.RandomState)

        return X_train, X_test, y_train, y_test

    def fit(self, numerical_method = StandardScaler(), categorical_method = OneHotEncoder(handle_unknown='ignore', sparse_output=False)): # Able to choose methods to scale features 
        full_pipe = self.__prepare_data(numerical_method , categorical_method)

        X_train, X_test, y_train, y_test = self.__split()

        if self.EnsembleBoolean:
            if self.NeuralBoolean:
                models = self.Regression_Models + self.Ensemble_Regression_Models + self.Neural_Regression_Models 
            else:
                models = self.Regression_Models + self.Ensemble_Regression_Models
        else:
            if self.NeuralBoolean:
                models = self.Regression_Models + self.Neural_Regression_Models
            else:
                models = self.Regression_Models

        for i in tqdm(range(len(models))):
            name, model = models[i]

            # Utilize the pipeline from earlier
            model_pipeline = make_pipeline(full_pipe, model)

            # Train the model
            model_pipeline.fit(X_train, y_train)

            # Make predictions on the test set
            y_pred = model_pipeline.predict(X_test)

            # Add to self.PredictedVal
            self.PredictedVal[name] = [y_test, y_pred]

        return self.PredictedVal # A dictionary of name, predicted values, actual values 

    def __calculate_accuracy(self):

        score = Score(self.PredictedVal, self.OutputType)    
        self.Scores = score.calculate() # Contains dict{Name-of-model: {metrics_name:metrics_val} }
        # self.Scores should be used as parameter to plot function

        return 

    def plot(self, metric): # Should plot the metrics

        self.__calculate_accuracy() # Would remove the unnecessary step of performing .calculate_accuracy() by the user
        plot = Plot(self.Scores, metric)
        plot.calculate()
        self.outlier_values = plot.display()

        return  