import csv
from google.cloud import storage
from joblib import dump
from datetime import datetime
import pickle
from modules.config.job_config import data_schema

def save_output_data(df, output_path, schema='prediction', run_env='local'):
    columns = data_schema[schema] 
    df = df[columns] 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{schema}_data_{timestamp}.csv"
    if run_env == 'local':
        save_output_data_local(df, output_path, filename)
    elif run_env == 'gcs':
        save_output_data_gcs(df, output_path, filename)
    else:
        raise ValueError("Invalid run_env value. It should be either 'local' or 'gcs'.")

def save_output_data_local(df, path, filename):
    df.to_csv(path + filename)
    print(f"Data saved locally: {path}")
    return f"{path}/{filename}"

def save_output_data_gcs(df, path, filename):
    storage_client = storage.Client()
    bucket_name, blob_name = parse_gcs_path(path, filename)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(df.to_csv(), content_type='text/csv')
    print(f"Data saved to GCS: {path}")
    return f"{path}/{filename}"

def parse_gcs_path(gcs_path, filename):
    gcs_path = gcs_path.replace('gs://', '')
    parts = gcs_path.split('/')
    bucket_name = parts[0]
    blob_name = '/'.join(parts[1:])
    blob_name = f"{blob_name}/{filename}"
    print(blob_name)
    return bucket_name, blob_name