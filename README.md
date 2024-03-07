# MLProjectTemplate

## Setup

### 1
#### Set up virtual env
conda create -n venv-template python=3.10
conda activate venv-template
pip install -r requirements.txt
#### Run
Make sure your launch.json file is up to date and using your desired arguments and run with vscode debugger

OR

python run.py --input_data_path ./local/sample_data.csv --output_data_path ./local/ --model_path ./local/models/model_20240307_054739.joblib --pipeline_path ./local/models/data_prep_pipeline_20240307_054705.joblib --run_env local

python run.py --input_data_path gs://ml-project-template/input_data/sample_data.csv --output_data_path gs://ml-project-template/output_data --pipeline_path gs://ml-project-template/model/data_prep_pipeline_20240306_235640.joblib  --model_path gs://ml-project-template/model/model_20240306_235700.joblib --run_env gcs

OR
### 2
#### Build a package
python setup.py install

OR
### 3
#### Set up docker 
##### (Ensure docker is installed on your machine)
https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images#get-image
https://medium.com/@abhinav.90444/title-pushing-artifacts-to-artifact-registry-a-step-by-step-guide-97f825242cfc

docker build -t myapp-pred .

docker run myapp-pred --input_data_path ./local/sample_data.csv --output_data_path ./local/ --model_path ./local/models/model_20240307_054739.joblib --pipeline_path ./local/models/data_prep_pipeline_20240307_054705.joblib --run_env local

docker run myapp-pred --input_data_path gs://ml-project-template/input_data/sample_data.csv --output_data_path gs://ml-project-template/output_data --pipeline_path gs://ml-project-template/model/data_prep_pipeline_20240306_235640.joblib  --model_path gs://ml-project-template/model/model_20240306_235700.joblib --run_env gcs

## Artifact Registry
GCP - Artifact registry
gcloud auth configure-docker us-central1-docker.pkg.dev
docker tag myapp us-central1-docker.pkg.dev/<project-id>/ml-project-template/myapp:dev
<!-- docker pull us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0 -->
docker push us-central1-docker.pkg.dev/<project-id>/ml-project-template/myapp:dev

## Run on vertex AI
gcloud ai custom-jobs create --region=us-central1 --display-name=training_test_cli3 --worker-pool-spec=machine-type=n1-standard-4,replica-count=1,container-image-uri=us-central1-docker.pkg.dev/<project-id>/ml-project-template/myapp:dev --worker-pool-spec=machine-type=n1-standard-4,replica-count=1,container-image-uri=us-central1-docker.pkg.dev/<project-id>/ml-project-template/myapp:dev --args="--input_data_path=gs://ml-project-template/input_data/sample_data.csv,--output_data_path=gs://ml-project-template/output_data/test_out,--model_path=gs://ml-project-template/model,--run_env=gcs"