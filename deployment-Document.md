# Azure AKS Deployment Guide

This document explains how to deploy the application from a local machine to Azure Kubernetes Service (AKS).

Deployment Flow: Local Application → Docker Image → Azure Container Registry (ACR) → Azure Kubernetes Service (AKS) → Azure PostgreSQL → Public Load Balancer → Application URL

## Steps

1. `docker build -t invint .`
2. `docker tag invint:latest invintelligence.azurecr.io/invint:v1`
3. `az acr login --name invintelligence`
4. `docker push invintelligence.azurecr.io/invint:v1`
5. `az aks get-credentials --resource-group rg-inv-intelligence --name inv-intelligence-aks`
6. `kubectl apply -f k8s/deployment.yaml`
7. `kubectl apply -f k8s/service.yaml`
8. `kubectl get svc` — get the external IP
9. Open `http://<external-ip>` in browser

## Troubleshooting

- `kubectl get pods` — check pod status
- `kubectl logs <pod-name>` — view logs
- `kubectl describe pod <pod-name>` — detailed pod info
- `kubectl rollout restart deployment/invint` — restart deployment
