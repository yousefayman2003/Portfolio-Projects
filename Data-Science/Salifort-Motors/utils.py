"""Module containing helper functions for the notebook"""
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def write_pickle(path, model_object, save_as:str):
    '''
        Args: 
            path:         path of folder where you want to save the pickle
            model_object: a model you want to pickle
            save_as:      filename for how you want to save the model

        Return: A call to pickle the model in the folder indicated
    '''    

    with open(path + save_as + '.pickle', 'wb') as to_write:
        pickle.dump(model_object, to_write)
        
def read_pickle(path, saved_model_name:str):
    '''
        Args: 
            path:             path to folder where you want to read from
            saved_model_name: filename of pickled model you want to read in

        Returns: 
            model: the pickled model 
    '''
    with open(path + saved_model_name + '.pickle', 'rb') as to_read:
        model = pickle.load(to_read)

    return model

def get_scores(model_name:str, model, X_test_data, y_test_data):
    '''
        Generate a table of test scores.

        Args: 
            model_name (string):  How you want your model to be named in the output table
            model:                A fit GridSearchCV object
            X_test_data:          numpy array of X_test data
            y_test_data:          numpy array of y_test data

        Returns: pandas df of precision, recall, f1, accuracy, and AUC scores for your model
    '''

    preds = model.best_estimator_.predict(X_test_data)

    auc = roc_auc_score(y_test_data, preds)
    accuracy = accuracy_score(y_test_data, preds)
    precision = precision_score(y_test_data, preds)
    recall = recall_score(y_test_data, preds)
    f1 = f1_score(y_test_data, preds)

    table = pd.DataFrame({'model': [model_name],
                          'precision': [precision], 
                          'recall': [recall],
                          'f1': [f1],
                          'accuracy': [accuracy],
                          'AUC': [auc]
                         })
  
    return table