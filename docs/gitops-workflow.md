# GitOps Workflow Guide

This document explains the complete GitOps workflow implemented in this project using GitHub Actions, Amazon ECR, ArgoCD, and Amazon EKS.

---

# What is GitOps?

GitOps is an operational framework that uses Git as the single source of truth for infrastructure and application deployments.

Benefits:

* Automated Deployments
* Version Controlled Infrastructure
* Easy Rollbacks
* Auditability
* Declarative Configuration
* Self-Healing Infrastructure

---

# GitOps Architecture

```text
Developer
    ↓
GitHub Repository
    ↓
GitHub Actions (CI)
    ↓
Build Docker Image
    ↓
Push Image to Amazon ECR
    ↓
Update GitOps Repository
    ↓
ArgoCD Detects Change
    ↓
Sync to Kubernetes
    ↓
Application Updated
```

---

# Repository Structure

```text
cloud-native-devops-pipeline/

├── .github/workflows/
│   ├── CI.yaml
│   ├── CD.yaml
│   └── infra-provision.yaml
│
├── terraform/
│   ├── Infrastructure/
│   └── Cluster-Bootstrap/
│
├── gitops-k8s/
│   ├── application/
│   ├── monitoring/
│   ├── logging/
│   ├── monitoring-crds/
│   └── app-of-apps/
│
├── frontend/
├── backend/
└── docs/
```

---

# GitOps Components

## GitHub

Acts as:

* Source Code Repository
* GitOps Repository
* Workflow Trigger Source

---

## GitHub Actions

Handles:

* Build Automation
* Docker Image Creation
* Image Push to ECR
* GitOps Repository Updates

---

## Amazon ECR

Acts as:

* Container Registry
* Image Storage
* Deployment Source

---

## ArgoCD

Responsible for:

* Git Repository Monitoring
* State Reconciliation
* Automated Synchronization
* Drift Detection
* Self-Healing

---

## Amazon EKS

Runs:

* Frontend Application
* Backend Application
* Monitoring Stack
* Logging Stack

---

# Infrastructure Provision Workflow

Infrastructure deployment is triggered manually.

Workflow:

```text
GitHub Actions
    ↓
Terraform Init
    ↓
Terraform Plan
    ↓
Terraform Apply
    ↓
AWS Infrastructure Created
```

Resources Created:

* VPC
* Subnets
* Internet Gateway
* NAT Gateway
* Security Groups
* EKS Cluster
* ECR Repository
* RDS PostgreSQL

---

# Continuous Integration (CI)

CI starts automatically when code is pushed.

Workflow:

```text
Developer Push
    ↓
GitHub Actions
    ↓
Build Application
    ↓
Build Docker Image
    ↓
Push Image to ECR
```

---

# CI Process

## Step 1

Developer pushes code.

```bash
git push origin main
```

---

## Step 2

GitHub Actions workflow starts.

Workflow file:

```text
.github/workflows/CI.yaml
```

---

## Step 3

Docker image is built.

Example:

```bash
docker build -t employee-management .
```

---

## Step 4

Authenticate with ECR.

```bash
aws ecr get-login-password
```

---

## Step 5

Push image to ECR.

```text
ECR Repository
↓
employee-management:latest
```

---

# Continuous Delivery (CD)

CD deployment is GitOps-based.

ArgoCD continuously monitors Git.

---

# CD Workflow

```text
New Image Available
        ↓
GitOps Repository Updated
        ↓
ArgoCD Detects Change
        ↓
Sync Triggered
        ↓
Kubernetes Deployment Updated
```

---

# Application Deployment Flow

```text
Developer
    ↓
Git Push
    ↓
GitHub Actions

Build
Test
Docker Build
Push to ECR

    ↓

Update Deployment Manifest

    ↓

GitOps Repository

    ↓

ArgoCD

    ↓

Kubernetes Deployment

    ↓

Frontend Pod
Backend Pod
```

---

# ArgoCD App of Apps Pattern

The project follows the App of Apps pattern.

Root Application:

```text
app-of-apps
```

Manages:

```text
application
monitoring-crds
prometheus
loki
promtail
```

Benefits:

* Centralized Management
* Easier Scaling
* Better Organization
* Dependency Management

---

# ArgoCD Reconciliation

ArgoCD continuously compares:

```text
Desired State (Git)
            VS
Actual State (Cluster)
```

---

# Self-Healing

If someone manually changes resources:

```bash
kubectl edit deployment
```

ArgoCD detects drift.

Automatically restores:

```text
Git State
↓
Cluster State
```

---

# Automated Sync

Applications use:

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
```

Meaning:

## Self Heal

Automatically corrects configuration drift.

---

## Prune

Removes resources deleted from Git.

---

# Deployment Order

Monitoring stack requires CRDs.

Deployment Order:

```text
monitoring-crds
        ↓
prometheus
        ↓
grafana
        ↓
alertmanager
```

This prevents resource creation failures.

---

# Sync Waves

Used to control deployment sequence.

Example:

```yaml
annotations:
  argocd.argoproj.io/sync-wave: "-1"
```

Meaning:

```text
Deploy First
```

Higher values deploy later.

---

# ArgoCD Health Verification

Check Applications:

```bash
kubectl get applications -n argocd
```

Expected:

```text
Healthy
Synced
```

---

# Verify ArgoCD Sync

```bash
argocd app list
```

or

```bash
kubectl get applications -n argocd
```

---

# Manual Sync

```bash
argocd app sync <app-name>
```

---

# Hard Refresh

```bash
kubectl annotate application <app-name> \
-n argocd \
argocd.argoproj.io/refresh=hard \
--overwrite
```

Useful after:

* CRD Changes
* Chart Upgrades
* Failed Syncs

---

# Rollback Strategy

GitOps enables simple rollback.

```text
Previous Commit
        ↓
Git Revert
        ↓
Push
        ↓
ArgoCD Sync
        ↓
Previous Version Restored
```

---

# Common GitOps Issues

## Application Out Of Sync

Verification:

```bash
kubectl get applications -n argocd
```

Resolution:

```bash
argocd app sync <app-name>
```

---

## Missing CRDs

Symptoms:

```text
no matches for kind
```

Resolution:

Deploy monitoring CRDs first.

---

## Sync Failed

Verify:

```bash
kubectl describe application <app-name> -n argocd
```

Check:

* Repository Access
* Manifest Errors
* CRD Dependencies

---

# Security Considerations

Current Project:

* GitHub OIDC Authentication
* IAM Role Assumption
* Private EKS Worker Nodes
* GitOps Deployment Model

Future Improvements:

* AWS Secrets Manager
* External Secrets Operator
* ArgoCD Image Updater
* RBAC Hardening

---

# Key Learnings

* Git is the single source of truth.
* ArgoCD continuously reconciles cluster state.
* App of Apps improves scalability.
* Self-Healing prevents configuration drift.
* CRD ordering is important for operator-based applications.
* GitOps provides repeatable and auditable deployments.
* Rollbacks become significantly easier.
* Infrastructure and applications can be managed declaratively.
