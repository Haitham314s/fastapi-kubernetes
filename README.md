# Ecommerce microservice architecture

## Powered by FastAPI, PostgreSQL, Kubernetes, Minikube EKS (Elastic Kubernetes Service), Helm Charts, AWS, Redis & Celery

### Covered with unit testing of all current APIs via asynchronous pytest

# Run Celery worker command

```
celery -A main.celery worker -l info --pool=prefork
```

# Steps to run k8s microservices

1. Install minikube, kubectl, docker desktop
2. Run minikube command:

```
minikube start --mount-string="$HOME/postgres-data:/postgres-data" --mount --driver=docker --install-addons=true --kubernetes-version=stable
```

3. Run kubernetes files the imperative way:

```
cd k8s/
kubectl apply -f ./<DIRECTORY>
```
