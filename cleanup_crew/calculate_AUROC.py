import json
from sklearn.metrics import roc_auc_score
import numpy as np

def calculate_AUROC(json_file):
    y_true = np.tile([1, 0], len(json_file))
    predictions = np.array([
    val for instance in json_file.values()
    for val in (instance["lxmert"]["caption"], instance["lxmert"]["foil"])])
    
    
    print("true: ", y_true)
    print("------------")
    print("pred: ", predictions)
    AUROC_score = roc_auc_score(y_true, predictions)
    return AUROC_score

