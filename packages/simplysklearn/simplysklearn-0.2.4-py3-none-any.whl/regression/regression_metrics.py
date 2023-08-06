from sklearn.metrics import explained_variance_score, max_error, mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, r2_score, mean_absolute_percentage_error, d2_absolute_error_score, d2_pinball_score, d2_tweedie_score
from sklearn.preprocessing import minmax_scale

class Score():
    def __init__(self, data):
        self.res = {} # dict{Name-of-model: {metrics_name:metrics_val} }
        self.data = data
        # data is in the type {name-of-model : [y_true, y_pred]}

    def calculate(self):
        keys = list(self.data.keys())
        print(f"Calculating error metrics\n")
        for i in range(len(self.data)): # Looping over different models 
                key = keys[i] # key => model names 
                y_true, y_pred = self.data[key][0], self.data[key][1]
                self.res[key] = {}
                self.res[key]['explained_variance'] = explained_variance_score(y_true, y_pred)
                self.res[key]['max_error'] = max_error(y_true, y_pred)
                self.res[key]['mean_absolute_error'] = mean_absolute_error(y_true, y_pred)
                self.res[key]['mean_squared_error'] = mean_squared_error(y_true, y_pred)
                self.res[key]['mean_squared_log_error'] = mean_squared_log_error(minmax_scale(y_true, feature_range=(0,1)), minmax_scale(y_pred, feature_range=(0,1)))
                self.res[key]['median_absolute_error'] = median_absolute_error(y_true, y_pred)
                self.res[key]['r2_score'] = r2_score(y_true, y_pred)
                self.res[key]['mean_absolute_percentage_error'] = mean_absolute_percentage_error(y_true, y_pred)
                self.res[key]['d2_absolute_error_score'] = d2_absolute_error_score(y_true, y_pred)
                self.res[key]['d2_pinball_score'] = d2_pinball_score(y_true, y_pred)
                self.res[key]['d2_tweedie_score'] = d2_tweedie_score(y_true, y_pred)

        return self.res
