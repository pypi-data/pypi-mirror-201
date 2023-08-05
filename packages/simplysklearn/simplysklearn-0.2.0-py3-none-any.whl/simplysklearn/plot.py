import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd

class Plot:
    def __init__(self, data, metric):
        self.data = data
        self.metric_name = metric
        self.plot_data = {}
        self.non_plot_data = {}
        self.disppearing_ratio = 500 # The ratio at which to remove outliers (too large/small values)

    def calculate(self):

        for model in self.data: # model -> name of model

            if self.metric_name in self.data[model] and self.data[model][self.metric_name] != None: # If predict_proba = True and model has no predict_proba property (no y_pred)
                self.plot_data[model] = self.data[model][self.metric_name]
            else:
                self.non_plot_data[model] = None

        return self.plot_data

    def display(self):
        self.plot_data = dict(sorted(self.plot_data.items(), key=lambda item: item[1]* -1))

        # We have to filter out those values where it is too big/small so that they don't skew the plot O(N)
        keys = list(self.plot_data.keys())
        for i, model in enumerate(self.plot_data):
            val = self.plot_data[model]
            if i < len(self.plot_data)-1:
                next_val = self.plot_data[keys[i+1]]
            else:
                break

            if abs(val/next_val) > self.disppearing_ratio:
                self.non_plot_data[model] = val

        """for model in self.non_plot_data:
            del self.plot_data[model]"""

        # Making a dataframe to use with plotly
        df = pd.DataFrame({'Model':list(self.plot_data.keys()), 'Values':list(self.plot_data.values())})
    
        sns.set_theme()
        sns.set_context("paper")
        ax = sns.barplot(df, x='Values', y='Model').set(title=f'{" ".join(self.metric_name.split("_"))}')

        # Return non plottable data
        if len(self.non_plot_data) > 0:
            print(f"There were {len(self.non_plot_data)} number of non plottable data")

        plt.show()
        return self.non_plot_data if len(self.non_plot_data) > 0 else "No data points were removed"



"""
# Testing code

hi = {'Linear Regression': 5.945477578686267e+30, 'Gaussian Process Regressor': 38862842948.98595, 'MLP Regressor': 35413863580.22882, 'SVR': 7197385705.765231, 'Perceptron': 3634079418.0570774, 'Decision Tree Regressor': 2015704715.13242, 'ElasticNet': 1139044333.7945106, 'Ada Boost Regressor': 1114901189.166725, 'SGDRegressor': 963807765.7846137, 'ARDRegression': 881823520.212382, 'Lasso': 863589220.5745481, 'Bayesian Ridge': 862270354.5060233, 'Ridge': 814237316.0583718, 
'XGBRegressor': 757239500.2347634, 'Random Forest Regressor': 739429472.215051, 'Passive Aggressive Regressor': 731582371.3055538, 'Gradient Boosting Regressor': 633820421.5121104}
tmp = Plot(hi, 'mean_squared_error')
tmp.display()

"""
