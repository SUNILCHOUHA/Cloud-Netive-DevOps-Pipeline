# Deployment Guide

This document explains how to deploy the Cloud Native DevOps Pipeline on AWS using Terraform, GitHub Actions, ArgoCD, EKS, Prometheus, Grafana, Loki, and Promtail.

---

# Architecture Overview

The project provisions AWS infrastructure using Terraform and deploys applications through GitOps using ArgoCD.

```text
Developer
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Terraform
    ↓
AWS Infrastructure

VPC
EKS
ECR
RDS

    ↓

ArgoCD
    ↓

Applications
Monitoring
Logging

    ↓

Kubernetes Cluster
```

---

# Prerequisites

Install the following tools:

## AWS CLI

Verify:

```bash
aws --version
```

---

## Terraform

Verify:

```bash
terraform version
```

---

## kubectl

Verify:

```bash
kubectl version --client
```

---

## Git

Verify:

```bash
git --version
```

---

# Clone Repository

```bash
git clone <repository-url>

cd cloud-native-devops-pipeline
```

---

# Configure AWS Credentials

```bash
aws configure
```

Provide:

```text
AWS Access Key
AWS Secret Key
Region
Output Format
```

Verify:

```bash
aws sts get-caller-identity
```

---

# Infrastructure Deployment

Infrastructure provisioning is divided into two stages.

## Stage 1: Core Infrastructure

Components:

* VPC
* Public Subnets
* Private Subnets
* Internet Gateway
* NAT Gateway
* Security Groups
* EKS Cluster
* ECR Repository
* RDS PostgreSQL

Navigate:

```bash
cd terraform/Infrastructure
```

Initialize:

```bash
terraform init
```

Validate:

```bash
terraform validate
```

Plan:

```bash
terraform plan
```

Apply:

```bash
terraform apply
```

Verify:

```bash
aws eks list-clusters
```

---

## Update Kubeconfig

```bash
aws eks update-kubeconfig \
--region ap-south-1 \
--name <cluster-name>
```

Verify:

```bash
kubectl get nodes
```

Expected:

```text
Ready
```

for all worker nodes.

---

# Stage 2: Cluster Bootstrap

Components:

* ArgoCD
* Kubernetes Providers
* Helm Providers

Navigate:

```bash
cd terraform/Cluster-Bootstrap
```

Initialize:

```bash
terraform init
```

Plan:

```bash
terraform plan
```

Apply:

```bash
terraform apply
```

Verify:

```bash
kubectl get pods -n argocd
```

Expected:

```text
Running
```

for all ArgoCD components.

---

# Access ArgoCD

Retrieve Admin Password:

```bash
kubectl get secret argocd-initial-admin-secret \
-n argocd \
-o jsonpath="{.data.password}" | base64 -d
```

Port Forward:

```bash
kubectl port-forward svc/argocd-server \
-n argocd \
8080:443
```

Access:

```text
https://localhost:8080
```

---

# Deploy Monitoring CRDs

Prometheus Operator CRDs are managed separately.

Deploy:

```bash
kubectl apply --server-side -f monitoring-crds/
```

Verify:

```bash
kubectl get crd | grep monitoring.coreos.com
```

Expected:

```text
10 Prometheus Operator CRDs
```

---

# Deploy Applications

ArgoCD automatically deploys:

* Application Stack
* Prometheus
* Grafana
* Alertmanager
* Loki
* Promtail

Verify:

```bash
kubectl get applications -n argocd
```

Expected:

```text
Healthy
Synced
```

---

# Verify Application Deployment

```bash
kubectl get pods -A
```

Verify:

* Frontend Pods
* Backend Pods
* Monitoring Pods
* Logging Pods

---

# Verify Monitoring Stack

```bash
kubectl get pods -n monitoring
```

Expected Components:

```text
Prometheus
Grafana
Alertmanager
Prometheus Operator
Node Exporter
kube-state-metrics
Loki
Promtail
```

---

# Verify Alerting

Check Alert Rules:

```bash
kubectl get prometheusrules -n monitoring
```

Open Prometheus:

```text
Status → Alerts
```

Expected:

```text
Pending
Firing
```

when alerts are triggered.

---

# Verify Logging

Open Grafana.

Navigate:

```text
Explore → Loki
```

Verify:

```text
Application Logs
System Logs
ArgoCD Logs
```

are visible.

---

# Access Services

## Grafana

```bash
kubectl port-forward svc/prometheus-grafana \
-n monitoring \
3000:80
```

Access:

```text
http://localhost:3000
```

---

## Prometheus

```bash
kubectl port-forward \
svc/prometheus-kube-prometheus-prometheus \
-n monitoring \
9090:9090
```

Access:

```text
http://localhost:9090
```

---

## Employee Management Application

Retrieve Load Balancer:

```bash
kubectl get svc
```

Access application using generated Load Balancer URL.

---

# CI/CD Workflow

Developer pushes code.

```text
GitHub Push
    ↓
GitHub Actions
    ↓
Build Docker Image
    ↓
Push Image to ECR
    ↓
GitOps Repository Update
    ↓
ArgoCD Sync
    ↓
Deployment Update
```

---

# Validation Checklist

Infrastructure:

* VPC Created
* EKS Running
* ECR Available
* RDS Available

Cluster:

* Nodes Ready
* ArgoCD Healthy

Monitoring:

* Prometheus Running
* Grafana Running
* Alertmanager Running

Logging:

* Loki Running
* Promtail Running

Application:

* Frontend Accessible
* Backend Accessible
* Database Connected

CI/CD:

* Image Build Successful
* ECR Push Successful
* ArgoCD Sync Successful

---

# Cleanup

Destroy Cluster Bootstrap:

```bash
cd terraform/Cluster-Bootstrap

terraform destroy
```

Destroy Infrastructure:

```bash
cd terraform/Infrastructure

terraform destroy
```

Warning:

Destroying infrastructure will permanently delete:

* EKS Cluster
* RDS Database
* ECR Repository
* VPC Resources
