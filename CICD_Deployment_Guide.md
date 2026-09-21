# AKS CI/CD Deployment Reference Guide

This document explains the CI/CD pipeline fields used in `k8s/deployment.yaml`, `k8s/service.yaml`, and `.github/workflows/deploy.yaml`.

## GitHub Actions Workflow

The workflow triggers on push to `main` and performs:
1. Checkout repository
2. Login to Azure
3. Login to ACR
4. Build and push Docker image
5. Get AKS credentials
6. Create Kubernetes secrets
7. Apply deployment and service manifests
8. Restart and verify rollout

## Kubernetes Resources

### Deployment
- `replicas: 1` — single pod for cost efficiency
- `imagePullPolicy: Always` — ensures latest image on every deploy
- `envFrom.secretRef` — injects all secrets from Kubernetes secret

### Service
- `type: LoadBalancer` — creates Azure public IP
- `port: 80` → `targetPort: 8000` — routes public traffic to FastAPI

## Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | Azure service principal JSON |
| `ACR_NAME` | Azure Container Registry name |
| `ACR_LOGIN_SERVER` | ACR login server URL |
| `AKS_RESOURCE_GROUP` | AKS resource group name |
| `AKS_CLUSTER_NAME` | AKS cluster name |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint |
| `AZURE_SEARCH_ENDPOINT` | Azure AI Search endpoint |
| `POSTGRES_HOST` | PostgreSQL host |
