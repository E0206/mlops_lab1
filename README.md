# Lab 1: Your First Model Service on Kubernetes



This repository contains the implementation of Lab 1 from **MLOps Foundations & Cloud Native AI**.



The project demonstrates an end-to-end MLOps workflow, including machine learning model training, experiment tracking with MLflow, API development with FastAPI, Docker containerization, Kubernetes deployment, and automatic scaling using a Horizontal Pod Autoscaler (HPA).



## 1. Project Overview



The Iris dataset is used to train a Random Forest classifier with scikit-learn. MLflow tracks the training parameters, evaluation metrics, and trained model.



The model is then exposed through a FastAPI application, packaged into a Docker image, and deployed to a local Kubernetes cluster created with kind.



Finally, an HPA is configured to scale the application based on CPU utilization, and the scaling behavior is evaluated using HTTP load testing.



## 2. Technologies



- Python 3.11

- scikit-learn

- MLflow

- FastAPI and Uvicorn

- Docker

- kind and Kubernetes

- kubectl

- Kubernetes Metrics Server

- hey (HTTP load testing)



## 3. Repository Structure



```text

mlops-lab1/

├── train.py

├── app.py

├── model.joblib

├── Dockerfile

├── .dockerignore

├── .gitignore

├── requirements.txt

├── request.json

├── README.md

├── k8s/

│   ├── deployment.yaml

│   ├── service.yaml

│   └── hpa.yaml

└── screenshots/

&#x20;   ├── mlflow-run.png

&#x20;   └── hpa-scaling.png

```



## 4. Model Training and MLflow Tracking



Install the required Python dependencies:



```bash

pip install -r requirements.txt

```



Train the Iris classification model:



```bash

python train.py

```



The training script uses a Random Forest classifier with 100 estimators and an 80/20 train-test split.



MLflow records the model parameters, classification accuracy, and trained model artifacts.



Start the MLflow UI:



```bash

mlflow ui --port 5000

```



Open `http://localhost:5000` to inspect the `iris-classification` experiment.



### MLflow Run



![MLflow Run](screenshots/mlflow-run.png)



## 5. FastAPI Model Service



The trained classifier is exposed through two endpoints:



| Method | Endpoint | Description |

|---|---|---|

| POST | `/predict` | Predicts Iris flower classes |

| GET | `/healthz` | Returns the service health status |



Start the API locally:



```bash

uvicorn app:app --host 0.0.0.0 --port 8080

```



Example prediction request:



```json

{

&#x20; "instances": [

&#x20;   [5.1, 3.5, 1.4, 0.2]

&#x20; ]

}

```



Example response:



```json

{

&#x20; "predictions": [0]

}

```



## 6. Docker Containerization



Build the Docker image:



```bash

docker build -t iris-api:v1 .

```



The Dockerfile packages the trained model, FastAPI application, and inference dependencies into a container image.



## 7. Kubernetes Deployment



Create a local Kubernetes cluster:



```bash

kind create cluster --name mlops

```



Load the Docker image into kind:



```bash

kind load docker-image iris-api:v1 --name mlops

```



Deploy the application:



```bash

kubectl apply -f k8s/deployment.yaml

kubectl apply -f k8s/service.yaml

```



Verify the deployment:



```bash

kubectl get pods

kubectl get deployments

kubectl get svc

```



Forward the Kubernetes Service to the local machine:



```bash

kubectl port-forward svc/iris-api-svc 8081:80

```



The prediction API is then accessible through `http://localhost:8081/predict`.



## 8. Horizontal Pod Autoscaling



The HPA is configured with the following settings:



| Parameter | Value |

|---|---|

| Target Deployment | iris-api |

| Minimum Replicas | 1 |

| Maximum Replicas | 5 |

| Target CPU Utilization | 50% |



Metrics Server is required for CPU-based autoscaling.



Deploy the HPA:



```bash

kubectl apply -f k8s/hpa.yaml

```



Monitor scaling:



```bash

kubectl get hpa -w

```



Generate HTTP load using hey:



```bash

hey -z 3m -c 50 -m POST -T "application/json" -D request.json http://127.0.0.1:8081/predict

```



### HPA Scaling Results



During load testing, the CPU utilization increased significantly, triggering automatic scaling.



The number of replicas increased from **1 to 3 and subsequently to 5**, demonstrating that Kubernetes HPA successfully adjusted the deployment in response to increased CPU demand.



![HPA Scaling](screenshots/hpa-scaling.png)



## 9. Conclusion



This lab demonstrates how a machine learning model can be transformed into a containerized API service and deployed on Kubernetes.



MLflow enables experiment tracking, FastAPI provides model inference endpoints, Docker packages the application, and Kubernetes manages deployment and automatic scaling.



The HPA experiment successfully demonstrated CPU-based horizontal scaling from one replica to five replicas under increased request load.



