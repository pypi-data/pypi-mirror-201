import os
import sys
import uuid
import bq_utils
from datetime import date
import pandas as pd
import numpy as np
from sklearn.metrics import (mean_absolute_error, mean_absolute_percentage_error, 
                             mean_squared_error, confusion_matrix, r2_score)
from google.cloud import storage
from utils import Logger
LOGGER = Logger()
LOG = LOGGER.LOG

### CONSTANTS ###
today = date.today().strftime("%Y/%m/%d")
storage_client = storage.Client()
bucket_name = 'production-patternag-ds-ml-tracking'
home_dir = os.getcwd() + "/tmp"


tracker_columns = {
    'regression':['date','project','target_column','test_set','model','model_features',
                  'feature_importance','hyperparameters','mae','mape', 'rmse','mbe','rsquared',
                  'dataset_uri','prediction_uri','extra_parameters'],

    'classification':['date','project','target_column','test_set','model','model_features',
                      'feature_importance','hyperparameters','true_positive_rate',
                      'true_negative_rate',
                      'overall_accuracy','dataset_uri','prediction_uri','extra_parameters']
        }


def create_tracking_file(kind, project, new_csv):
    files = [f[0] for f in bq_utils.list_blobs(bucket_name, prefix=f'projects/{kind}')]
    projects = list(set([f.replace(f'gs://production-patternag-ds-ml-tracking/projects/{kind}/','').split("/")[0].split("_")[0] for f in files]))

    today = date.today().strftime("%Y/%m/%d").replace("/","")
    project_path = f'projects/{kind}'

    if project not in projects:
        LOG.info("No files associated with this project")
        LOG.info(f"Creating experiment tracker for '{project}' in projects/{kind}/")
        
        # create the empty sheet
        df = pd.DataFrame(columns=tracker_columns[kind])
        # save as a local csv
        tracking_log = f'{project}_{today}_1.csv'
        
        df.to_csv(f'{home_dir}/{tracking_log}', index=False)
        bq_utils.upload_blob(bucket_name, f'{home_dir}/{tracking_log}', f'{project_path}/{tracking_log}')
        # remove the local copy
        os.remove(f'{home_dir}/{tracking_log}')

    elif project in projects:
        LOG.info(f"Found tracking file(s) for '{project}':")
        
        blobs = bq_utils.list_blobs(bucket_name, prefix=f'projects/{kind}')
        blobs = [b for b in blobs if project in b[0]]
        newest_file = sorted(blobs, key=lambda tup: tup[1])[-1][0]

        if new_csv == True:
            tracking_log = make_new_csv(kind, project, newest_file)

        else:
            tracking_log = f'{newest_file.split("/")[-1]}'

    return tracking_log

def make_new_csv(kind, project, newest_file):
    today = date.today().strftime("%Y/%m/%d").replace("/","")
    
    filename =  newest_file.split("/")[-1].split("_")
    created_at = filename[1]
    i = int(filename[-1].split(".")[0])

    if created_at == today:
        i += 1
        new_log = f'{project}_{today}_{i}.csv'

    elif int(today) > int(created_at):
        new_log = f'{project}_{today}_1.csv'

    df = pd.DataFrame(columns=tracker_columns[kind])
    df.to_csv(f'{home_dir}/{new_log}', index=False)

    bq_utils.upload_blob(bucket_name, f'{home_dir}/{new_log}', f'projects/{kind}/{new_log}')
    # remove the local copy
    os.remove(f'{home_dir}/{new_log}')

    return new_log

def classification_rates(y_true, y_pred):
    '''
    Calculates all the relevant classification scores/performance metrics
    '''

    # create a confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # calculate all metrics
    FP = cm.sum(axis=0) - np.diag(cm)  
    FN = cm.sum(axis=1) - np.diag(cm)
    TP = np.diag(cm)
    TN = cm.sum() - (FP + FN + TP)

    # Sensitivity, hit rate, recall, or true positive rate
    TPR = (TP/(TP+FN))[0]
    # Specificity or true negative rate
    TNR = (TN/(TN+FP) )[0]

    # Overall accuracy
    ACC = (TP+TN)/(TP+FP+FN+TN)

    results = {'TPR': TPR,
               'TNR': TNR,
               'ACC' : ACC    
            }
    return results

def calculate_performance(kind, y_true, y_pred):
    '''
    Determines which perfomance metrics to calculate based on the `kind` param
    '''
    y_true=np.array(y_true)
    y_pred=np.array(y_pred)
    if kind == 'regression':
        MAE = mean_absolute_error(y_true, y_pred)
        MAPE = mean_absolute_percentage_error(y_true, y_pred)
        RMSE = mean_squared_error(y_true, y_pred, squared=False)
        MBE = np.mean(y_pred - y_true)
        R2 = r2_score(y_true, y_pred)
        results = {m:r for m,r in zip(['MAE','MAPE','RMSE','MBE','R_squared'],[MAE, MAPE, RMSE, MBE, R2])}

    elif kind == 'classification':

        results = classification_rates(y_true, y_pred)

    return results

def create_output_files(kind, predictions, pred_id, labels=None):
    '''
    Creates output files for features, test set, and predictions and stores them in the
    `output` folder in the project folder
    '''

    if kind == 'regression':
        # create predictions file
        predictions = predictions.round(2)
        predictions['uuid'] = pred_id
        predictions.to_csv(f'{home_dir}/{pred_id}_predictions.csv')
        
        # upload to bucket
        bq_utils.upload_blob(bucket_name, f'{home_dir}/{pred_id}_predictions.csv', f'outputs/{kind}/{pred_id}_predictions.csv')
        os.remove(f'{home_dir}/{pred_id}_predictions.csv')

    elif kind == 'classification':
        y_true = predictions['actuals'].values
        y_pred = predictions['predictions'].values

        cm = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=labels)
        cm_df = pd.DataFrame(cm, index=labels)
        cm_df.reset_index(inplace=True)
        cm_df.rename(columns={'index':'classes'}, inplace=True)

        n_cols_to_add = 5 - len(labels)
        for i in range(n_cols_to_add):
            cm_df[f'col_{i+len(labels)}'] = None


        cm_df['uuid'] = pred_id
        cm_df.columns = ['classes', 'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'uuid']

        for i in range(1,6):
            cm_df[f"header_{i}"] = None

        prev = None
        for i,row in cm_df.iterrows():
            
            if row['uuid'] == prev:
                pass

            else:
                for j,c in enumerate(labels):
                    cm_df.loc[i,f'header_{j+1}'] = c
            prev = row['uuid']

        # upload to bucket
        cm_df.to_csv(f'{home_dir}/{pred_id}_predictions.csv')
        bq_utils.upload_blob(bucket_name, f'{home_dir}/{pred_id}_predictions.csv', f'outputs/{kind}/{pred_id}_predictions.csv')
        os.remove(f'{home_dir}/{pred_id}_predictions.csv')

def format_entry(kind, project, parameters, extra_parameters, results, pred_id):
    '''
    Based on `kind`, sets up the record that will be logged in the experiment tracking file.
    Also handles any extra parameters the user want to track.
    '''
    try:
        m = parameters['model']
        feature_names = m.feature_names_in_
        feature_importances = m.feature_importances_

        imp = {f:round(i*100,2) for f,i in zip(feature_names, feature_importances)}

    except AttributeError:
        try:
            m = parameters['model']
            feature_names = m.feature_names_in_
            coef = m.coef_[0]
            LOG.info("""It looks like you're using a linear model, be careful when interpreting feature importance (which are the model coefficients) if you did not standardize your dataset prior to training and testing""")
            imp = {f:round(i,2) for f,i in zip(feature_names, coef)}
            
        except AttributeError:
            LOG.info("""Unable to pull feature importances, feature names, or model coefficients from your model; make sure you ran `fit()` on the model passed in""")
            sys.exit()

    if kind == 'regression':

        data = {'date': date.today().strftime("%Y-%m-%d"),
                'project':project,
                'target_column': parameters['target_column'],
                'test_set': list(parameters['test_set']),
                'model': str(parameters['model']).split("(")[0],
                'model_features': parameters['model'].feature_names_in_,
                'feature_importance': imp,
                'hyperparameters': parameters['model'].get_params(),
                'mae': results['MAE'],
                'mape': results['MAPE'],
                'rmse': results['RMSE'],
                'mbe': results['MBE'],
                'rsquared': results['R_squared'],
                'dataset_uri': parameters['dataset_uri'],
                'prediction_uri': pred_id,
                'extra_parameters': extra_parameters
                } 

    elif kind == 'classification':
        data = {'date': date.today().strftime("%Y-%m-%d"), 
                'project':project,
                'target_column': parameters['target_column'],
                'test_set': list(parameters['test_set']),
                'model': str(parameters['model']).split("(")[0],
                'model_features': parameters['model'].feature_names_in_,
                'feature_importance': imp,
                'hyperparameters': parameters['model'].get_params(),
                'true_positive_rate': results['TPR'],
                'true_negative_rate': results['TNR'],
                'overall_accuracy': results['ACC'][0],
                'dataset_uri': parameters['dataset_uri'],
                'prediction_uri': pred_id,
                'extra_parameters': extra_parameters
                }
    
    new_experiment = pd.DataFrame([data])
    new_experiment = new_experiment.round(2)
    
    return new_experiment

def append_experiment(tracking_log, kind, new_experiment):
    '''
    Adds a new row to the experiment tracker for the current experiment
    '''

    # read in the experiment tracker
    tracker = pd.read_csv(f"gs://{bucket_name}/projects/{kind}/{tracking_log}")

    # append a row
    updated_log = pd.concat([tracker, new_experiment], ignore_index=True)

    # save the file locally
    updated_log.to_csv(f'{home_dir}/{tracking_log}', index=False)

    bq_utils.upload_blob(bucket_name, f'{home_dir}/{tracking_log}', f'projects/{kind}/{tracking_log}')
    # remove the local copy
    os.remove(f'{home_dir}/{tracking_log}')

def check_parameters(parameters):
    err_dict = {
                'dataset_uri': 'pass in the path as a string to parameters["dataset_uri"] for the GCP bucket where dataset is being stored',
                'target_column': 'pass in the name of the column being predicted into parameters["target_column"]',
                'test_set': 'pass in the list of sample_uuids that make up the test set into parameters["test_set"]',
                'model': 'pass in the model object into parameters["model"]'
                }

    for key in err_dict.keys():
        if (key not in parameters.keys()):
            LOG.info(f"`{key}` is missing from parameter argument; {err_dict[key]}")
            sys.exit()

        elif (parameters[key] is None):
            LOG.info(f"`{key}` is missing from parameter argument; {err_dict[key]}")
            sys.exit()

def log_experiment(kind, project, parameters, y_true, y_pred, extra_parameters=None, new_csv=None):
    # create a /tmp folder for saving files locally before uploading to the bucket
    if 'tmp' not in os.listdir(os.getcwd()):
        os.mkdir('tmp')


    y_pred = list(y_pred)
    y_true = list(y_true)
    if len(y_pred) == len(y_true):
        predictions = pd.DataFrame(data={'actuals': y_true,
                                         'predictions': y_pred
                                        })
        
    else:
        LOG.info("y_true and y_pred have different lengths; double check these args")
        sys.exit()

    project = project.replace("/","-").replace("_","-").replace(" ","-")
    
    # generate unique uuid for this run
    pred_id = str(uuid.uuid4())
    check_parameters(parameters)

    tracking_log = create_tracking_file(kind, project, new_csv)

    LOG.info(f"Tracker to use: {tracking_log}")

    results = calculate_performance(kind, y_true, y_pred)

    if kind == 'classification':
        labels = sorted(parameters['model'].classes_)

    else:
        labels = None    

    # formats the experiment record to be appended to the experiment tracker 
    new_experiment = format_entry(kind, project, parameters, extra_parameters, results, pred_id)

    append_experiment(tracking_log, kind, new_experiment=new_experiment)
    
    create_output_files(kind, predictions, pred_id, labels)
    # create_dashboard_data()
    LOG.info("Outputs saved!")
    