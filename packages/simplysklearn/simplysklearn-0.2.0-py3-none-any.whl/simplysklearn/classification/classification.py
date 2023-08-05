import numpy as np 
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import xgboost as xgb
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression, SGDClassifier, RidgeClassifier, LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, ARDRegression, SGDRegressor, PassiveAggressiveRegressor, Perceptron
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier, RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from tqdm import tqdm

from simplysklearn.metrics import Score
from simplysklearn.plot import Plot

class Classification:
    def __init__(self, data, FeatureList, Target, PredictProba = False, EnsembleBoolean=True, NeuralBoolean=True, SplitRatio=0.3, Randomstate=42):
        # Any possible parameters 
        self.PredictProba = PredictProba
        if not type(self.PredictProba) is bool:
            raise TypeError("Only Boolean variables accepted for PredictProba parameter")

        self.OutputType = 'classification'
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

        self.Classification_Models = [['Ridge Classifier', RidgeClassifier()], ['SGD Classifier', SGDClassifier()], ['Logistic Regression', LogisticRegression()], 
        ['Passive Agressive Classifier', PassiveAggressiveClassifier()], ['SVC', svm.SVC()], ['KNN Classifier', KNeighborsClassifier()],
        ['GaussianNB', GaussianNB()], ['Decision Tree Classifier', DecisionTreeClassifier()]]
        self.Ensemble_Classification_Models = [['Random Forest Classifier', RandomForestClassifier()], ['Ada Boost Classifier',AdaBoostClassifier()],
        ['Gradient Boosting Classifier', GradientBoostingClassifier()]]
        self.Neural_Classification_Models = [['MLP CLassifier', MLPClassifier()]]

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

    def fit(self, numerical_method = StandardScaler(), categorical_method = OneHotEncoder(handle_unknown='ignore', sparse_output=False)):
        full_pipe = self.__prepare_data()

        X_train, X_test, y_train, y_test = self.__split()

        if self.EnsembleBoolean:
            if self.NeuralBoolean:
                models = self.Classification_Models + self.Ensemble_Classification_Models + self.Neural_Classification_Models
            else:
                models = self.Classification_Models + self.Ensemble_Classification_Models
        else:
            if self.NeuralBoolean:
                models = self.Classification_Models + self.Neural_Classification_Models
            else:
                models = self.Classification_Models

        for i in tqdm(range(len(models))):
            name, model = models[i]
            print(f"Fitting for model {name}\n")

            # Utilize the pipeline from earlier
            model_pipeline = make_pipeline(full_pipe, model)

            # Train the model
            model_pipeline.fit(X_train, y_train)

            # Make predictions on the test set
            if self.PredictProba:
                try:
                    y_pred = model_pipeline.predict_proba(X_test)[:,1]
                except: # When predict_proba fails 
                    print(f"Predict Proba failed with {name} model\n")
                    y_pred = None
            else:
                y_pred = model_pipeline.predict(X_test)

            # Add to self.PredictedVal
            self.PredictedVal[name] = [y_test, y_pred]

        return self.PredictedVal # A dictionary of name, predicted values, actual values 

    def __calculate_accuracy(self):

        score = Score(self.PredictedVal, self.OutputType)    
        self.Scores = score.calculate() # Contains dict{Name-of-model: {metrics_name:metrics_val} 
        # self.Scores should be used as parameter to plot function

        return 

    def plot(self, metric): # Should plot the metrics

        print(f"Calculating accuracy values for pedictions\n")
        self.__calculate_accuracy()
        plot = Plot(self.Scores, metric)
        plot.calculate()
        self.outlier_values = plot.display()

        return  


#------------------Testing Code-----------------------#

"""import pandas as pd
df = pd.read_csv('/Users/kimhyunbin/Documents/Python/My own project (Python)/simplysklearn/tests/classification_2.csv')
model = Classification(df, df.columns.tolist()[1:-1], 'Class', PredictProba = True, EnsembleBoolean=False, NeuralBoolean=False, SplitRatio=0.3)
model.fit()
model.plot('log_loss')
print(model.outlier_values)"""