from sklearn.metrics import accuracy_score, balanced_accuracy_score, average_precision_score, brier_score_loss, f1_score, log_loss, precision_score, recall_score, jaccard_score, roc_auc_score, explained_variance_score, max_error, mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, r2_score, mean_absolute_percentage_error, d2_absolute_error_score, d2_pinball_score, d2_tweedie_score
from sklearn.preprocessing import minmax_scale
from tqdm import tqdm

class Score():
    def __init__(self, data, OutputType):
        self.res = {} # dict{Name-of-model: {metrics_name:metrics_val} }
        self.data = data
        self.task = OutputType
        # data is in the type {name-of-model : [y_true, y_pred]}

    def calculate(self):
        keys = list(self.data.keys())
        if self.task == 'regression':
            for i in tqdm(range(len(self.data))): # Looping over different models 
                key = keys[i] # key => model names 
                y_true, y_pred = self.data[key][0], self.data[key][1]
                self.res[key] = {}
                if y_pred != None:
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

        else: # Task is classification 
            for i in tqdm(range(len(self.data))): # Looping over different models 
                key = keys[i]
                y_true, y_pred = self.data[key][0], self.data[key][1]
                self.res[key] = {}

                # Calculating possible scores
                # try;except for models where predict_proba doesn't work -> in this case the score would reflect None
                # For None scores, we won't plot them 
                try: # In case y_pred is None
                    
                    try: # These do not support decimal point prediction values (no support for predict_proba)
                        self.res[key]['accuracy_score'] = accuracy_score(y_true, y_pred)
                    except:
                        self.res[key]['accuracy_score'] = None
                    
                    try:
                        self.res[key]['balanced_accuracy_score'] = balanced_accuracy_score(y_true, y_pred)
                    except:
                        self.res[key]['balanced_accuracy_score'] = None                    

                    try:
                        self.res[key]['f1_score'] = f1_score(y_true, y_pred)
                    except:
                        self.res[key]['f1_score'] = None

                    try:
                        self.res[key]['precision_score'] = precision_score(y_true, y_pred)
                    except:
                        self.res[key]['precision_score'] = None

                    try:
                        self.res[key]['recall_score'] = recall_score(y_true, y_pred)
                    except:
                        self.res[key]['recall_score'] = None

                    try:
                        self.res[key]['jaccard_score'] = jaccard_score(y_true, y_pred)
                    except:
                        self.res[key]['jaccard_score'] = None

                    self.res[key]['roc_auc_score'] = roc_auc_score(y_true, y_pred)
                    self.res[key]['log_loss'] = log_loss(y_true, y_pred)
                    self.res[key]['average_precision_score'] = average_precision_score(y_true, y_pred)
                    self.res[key]['brier_score_loss'] = brier_score_loss(y_true, y_true)

                except:
                    continue

        return self.res
