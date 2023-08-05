from sklearn.metrics import accuracy_score, balanced_accuracy_score, average_precision_score, brier_score_loss, f1_score, log_loss, precision_score, recall_score, jaccard_score, roc_auc_score

class Score():
    def __init__(self, data):
        self.res = {} # dict{Name-of-model: {metrics_name:metrics_val} }
        self.data = data
        # data is in the type {name-of-model : [y_true, y_pred]}

    def calculate(self):
        keys = list(self.data.keys())
        
        for i in range(len(self.data)): # Looping over different models 
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

                    try:
                        self.res[key]['roc_auc_score'] = roc_auc_score(y_true, y_pred)
                    except:
                        self.res[key]['roc_auc_score'] = None

                    try:
                        self.res[key]['log_loss'] = log_loss(y_true, y_pred)
                    except:
                        self.res[key]['log_loss'] = None

                    try:
                        self.res[key]['average_precision_score'] = average_precision_score(y_true, y_pred)
                    except:
                        self.res[key]['average_precision_score'] = None
                    
                    try:
                        self.res[key]['brier_score_loss'] = brier_score_loss(y_true, y_true)
                    except:
                        self.res[key]['brier_score_loss'] = None

                except:
                    continue

        return self.res