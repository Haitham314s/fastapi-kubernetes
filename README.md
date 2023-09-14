# Ecommerce microservice architecture

Powered by FastAPI, PostgreSQL, Kubernetes, Minikube EKS (Elastic Kubernetes Service), Helm Charts, AWS, Redis & Celery

Covered with unit testing of all current APIs via asynchronous pytest

## Install all dependencies and packages before proceeding

1. Minikube
2. Docker desktop
3. Helm

## Install python dependencies

    python -m venv venv
    ./venv/Scripts/activate

    OR

    source venv/Scripts/activate (for MacOS)
    pip install -r requirements.txt

## Run Celery worker command locally

    celery -A main.celery worker -l info --pool=prefork

## Start minikube cluster

    minikube start --mount-string="$HOME/postgres-data:/postgres-data" --mount --driver=docker --install-addons=true --kubernetes-version=stable

## Run all kubernetes manifests

    cd k8s/
    kubectl apply -f ./namespace
    kubectl apply -f ./postgres
    kubectl apply -f ./redis
    kubectl apply -f ./code
    kubectl apply -f ./celery
    kubectl apply -f ./nginx
    kubectl apply -f ./job

## Start Helm charts

    helm install myapp fastapi-helm --namespace ecommerce-fastapi --create-namespace
