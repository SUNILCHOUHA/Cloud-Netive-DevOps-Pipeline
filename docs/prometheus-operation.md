# Prometheus Operations Guide

This document explains the monitoring, alerting, logging, dashboards, and operational procedures used in the Cloud Native DevOps Pipeline project.

---

# Monitoring Architecture

The project uses the following observability stack:

```text
Prometheus
    ↓
Alertmanager
    ↓
Email Notifications

Prometheus
    ↓
Grafana
    ↓
Dashboards

Promtail
    ↓
Loki
    ↓
Grafana
```

---

# Components Overview

## Prometheus

Responsibilities:

* Metrics Collection
* Time Series Storage
* PromQL Query Engine
* Alert Evaluation

Collects metrics from:

* Kubernetes Nodes
* Pods
* Containers
* Applications
* kube-state-metrics
* Node Exporter

---

## Alertmanager

Responsibilities:

* Alert Processing
* Alert Grouping
* Alert Routing
* Email Notifications

Configured using Gmail SMTP.

Example Alerts:

* High CPU Usage
* High Memory Usage
* Pod Restarts
* Node Down

---

## Grafana

Responsibilities:

* Dashboard Visualization
* Alert Analysis
* Metrics Exploration
* Log Visualization

---

## Loki

Responsibilities:

* Log Aggregation
* Log Storage
* Log Querying

---

## Promtail

Responsibilities:

* Log Collection
* Kubernetes Pod Log Shipping
* Log Forwarding to Loki

---

# Monitoring Stack Verification

Check Monitoring Pods:

```bash
kubectl get pods -n monitoring
```

Expected Components:

```text
prometheus
grafana
alertmanager
prometheus-operator
node-exporter
kube-state-metrics
loki
promtail
```

---

# Access Grafana

Port Forward:

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

# Access Prometheus

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

# Prometheus Targets Verification

Open:

```text
Status → Targets
```

All targets should show:

```text
UP
```

Important Targets:

* kube-state-metrics
* node-exporter
* prometheus
* alertmanager

---

# Important PromQL Queries

## CPU Usage %

```promql
100 - (
avg by(instance)
(rate(node_cpu_seconds_total{mode="idle"}[5m]))
* 100
)
```

Purpose:

Calculates CPU utilization percentage.

Example:

```text
Idle = 95%
CPU Usage = 5%
```

---

## Memory Usage %

```promql
(
1 -
(
node_memory_MemAvailable_bytes
/
node_memory_MemTotal_bytes
)
) * 100
```

Purpose:

Calculates RAM usage percentage.

Example:

```text
Total Memory = 8 GB
Available = 2 GB

Used = 6 GB

Usage = 75%
```

---

## Disk Usage %

```promql
100 -
(
node_filesystem_avail_bytes
/
node_filesystem_size_bytes
* 100
)
```

Purpose:

Monitors filesystem utilization.

---

## Node Availability

```promql
up
```

Output:

```text
1 = Healthy
0 = Down
```

---

## Container Restarts

```promql
kube_pod_container_status_restarts_total
```

Purpose:

Tracks container restart count.

---

## Pod Count

```promql
count(kube_pod_info)
```

Purpose:

Displays total running pods.

---

## Network Receive

```promql
rate(node_network_receive_bytes_total[5m])
```

Purpose:

Network incoming traffic.

---

## Network Transmit

```promql
rate(node_network_transmit_bytes_total[5m])
```

Purpose:

Network outgoing traffic.

---

# Alerting Configuration

Alerting Flow:

```text
Prometheus
    ↓
PrometheusRule
    ↓
Alertmanager
    ↓
Gmail SMTP
    ↓
Email Notification
```

---

# Sample Alert Rule

```yaml
- alert: HighCPUUsage

  expr: |
    100 -
    (
      avg by(instance)
      (
        rate(
          node_cpu_seconds_total{mode="idle"}[5m]
        )
      ) * 100
    ) > 5

  for: 30s

  labels:
    severity: warning

  annotations:
    summary: High CPU Usage
    description: CPU usage is above 5%
```

---

# Alert States

## Inactive

Condition not met.

```text
No Alert
```

---

## Pending

Condition met but waiting for:

```yaml
for: 30s
```

---

## Firing

Condition remains true after waiting period.

Email notification sent.

---

# Alert Verification

Check Rules:

```bash
kubectl get prometheusrules -n monitoring
```

Check Alerts:

```text
Prometheus
↓
Alerts
```

Possible States:

```text
Inactive
Pending
Firing
```

---

# Alertmanager Verification

Verify Alertmanager Pods:

```bash
kubectl get pods -n monitoring
```

Check Logs:

```bash
kubectl logs \
alertmanager-prometheus-kube-prometheus-alertmanager-0 \
-n monitoring
```

---

# Verify Active Configuration

```bash
kubectl exec -it \
alertmanager-prometheus-kube-prometheus-alertmanager-0 \
-n monitoring -- sh
```

```bash
cat /etc/alertmanager/config_out/alertmanager.env.yaml
```

Verify:

```text
smtp_smarthost
smtp_auth_username
gmail-alerts
```

are present.

---

# Logging Architecture

```text
Application Logs
        ↓
Promtail
        ↓
Loki
        ↓
Grafana
```

---

# Verify Loki

```bash
kubectl get pods -n monitoring
```

Expected:

```text
loki
```

Running.

---

# Verify Promtail

```bash
kubectl get pods -n monitoring
```

Expected:

```text
promtail
```

Running.

---

# Grafana Dashboards

The project includes custom dashboards.

---

## Cluster Health Dashboard

Metrics:

* Total Nodes
* Total Pods
* Container Restarts
* Average CPU Usage

Purpose:

Cluster overview.

---

## Node Monitoring Dashboard

Metrics:

* CPU Usage
* Memory Usage
* Disk Usage
* Network Traffic

Purpose:

Node-level monitoring.

---

## Application Dashboard

Metrics:

* Frontend CPU
* Backend CPU
* Frontend Memory
* Backend Memory
* Pod Restarts

Purpose:

Application monitoring.

---

## GitOps Dashboard

Metrics:

* ArgoCD Pods
* ArgoCD Resource Usage
* ArgoCD Restarts

Purpose:

GitOps visibility.

---

## Logging Dashboard

Metrics:

* API Request Rate
* Error Count
* Backend Logs
* Monitoring Stack Logs

Purpose:

Centralized log analysis.

---

# Operational Commands

## Check Monitoring Resources

```bash
kubectl get all -n monitoring
```

---

## Check Prometheus Rules

```bash
kubectl get prometheusrules -n monitoring
```

---

## Check ServiceMonitors

```bash
kubectl get servicemonitors -n monitoring
```

---

## Check Targets

```bash
kubectl port-forward \
svc/prometheus-kube-prometheus-prometheus \
-n monitoring \
9090:9090
```

Navigate:

```text
Status → Targets
```

---

## Restart Prometheus

```bash
kubectl rollout restart statefulset \
prometheus-prometheus-kube-prometheus-prometheus \
-n monitoring
```

---

## Restart Alertmanager

```bash
kubectl rollout restart statefulset \
alertmanager-prometheus-kube-prometheus-alertmanager \
-n monitoring
```

---

## Restart Operator

```bash
kubectl rollout restart deployment \
prometheus-kube-prometheus-operator \
-n monitoring
```

---

# Troubleshooting

## CRD Missing

Symptoms:

```text
no matches for kind
```

Resolution:

```bash
kubectl get crd | grep monitoring.coreos.com
```

Ensure Prometheus Operator CRDs are installed before deploying Prometheus.

---

## CRD Installation Error

Symptoms:

```text
metadata.annotations: Too long
```

Resolution:

```bash
kubectl apply --server-side -f .
```

or

```yaml
syncOptions:
  - ServerSideApply=true
```

---

## Alert Emails Not Received

Check:

* Gmail App Password
* SMTP Credentials
* Alertmanager Logs
* Alertmanager Active Config

Verify:

```bash
cat /etc/alertmanager/config_out/alertmanager.env.yaml
```

---

## Application Healthy but Sync Failed

Possible Cause:

Historical ArgoCD Sync Failure.

Verify:

```bash
kubectl get applications -n argocd
```

If:

```text
Healthy
Synced
```

Current deployment is functioning correctly.

---

# Lessons Learned

* Prometheus Operator requires CRDs before deployment.
* Server-side apply is required for some large CRDs.
* PromQL is essential for monitoring and alerting.
* Alertmanager configuration should always be verified from the running pod.
* Grafana dashboards provide quick operational visibility.
* Loki and Promtail enable centralized Kubernetes logging.
* GitOps simplifies monitoring stack management through ArgoCD.
