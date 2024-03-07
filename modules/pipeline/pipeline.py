# Uses config, io and ml

from modules.io.read_data import get_data, load_model, load_pipeline
from modules.io.save_data import save_output_data
from modules.config.job_config import training_data_columns

def build_pipeline(options=dict):
    # Load Data
    df_raw = get_data(options.input_data_path, options.run_env)
    # Load Transformation
    data_prep_pipeline = load_pipeline(options.pipeline_path, options.run_env)
    # Load Model
    trained_model = load_model(options.model_path, options.run_env)

    # DEBUG only: print data - health checks
    print(df_raw.head(2))

    # Transform using data prep pipeline
    df = data_prep_pipeline.transform(df_raw)

    # DEBUG only: print data - health checks
    print(df.head(3))
    
    features = df[training_data_columns]

    # generate model predictions
    predictions = trained_model.predict(features)

    # DEBUG only: print data - health checks
    print(predictions)

    df['predictions'] = predictions

    # Save evaluation details
    save_output_data(df, options.output_data_path, 'prediction', options.run_env)