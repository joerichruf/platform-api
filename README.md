# Development

## Prerequisites

### Install k3d (Ubuntu)

```bash
# Install k3d
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Create a local cluster
k3d cluster create local

# Verify installation
kubectl get nodes
```

## Installing the project

```bash
poetry install
```

## Running the API

```bash
# Start the FastAPI server
poetry run uvicorn src.platform_api.main:app --reload

# The API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

## API Endpoints

### Health Check
- `GET /health` - Health status

### Deployments
- `POST /deployments` - Create deployment request
- `GET /deployments/namespaces/{namespace}/pods` - Get pods in namespace

## Testing

```bash
# Test the pods endpoint
curl http://localhost:8000/deployments/namespaces/default/pods
```
