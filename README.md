# DevSecOps Cyshield Assessment

This repository contains my solutions for the DevSecOps assessment, covering Bash scripting, Kubernetes infrastructure, application deployment, networking, security, observability, and CI/CD automation.

## Repository Structure

```text
.
├── task-1-bash/
├── task-2-kubernetes/
├── task-3-cicd/
└── README.md
```

---

# Repository Links

## GitHub Repository

[DevSecOps-Cyshield-Assessment (GitHub)](https://github.com/OmarZakaria10/DevSecOps-Cyshield-assessment?utm_source=chatgpt.com)

## GitLab Repository

Task 3 CI/CD pipeline execution, container registry integration, security scanning, and deployment stages were implemented and validated using GitLab:

[DevSecOps-Cyshield-Assessment (GitLab)](https://gitlab.com/OmarZakaria10/devsecops-cyshield-assessment?utm_source=chatgpt.com)

---

# Branch Strategy

To make the assessment easier to review and to clearly demonstrate the evolution of each task, I worked using dedicated branches for each deliverable.

| Branch              | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `task-1-bash`       | Bash scripting solution                                    |
| `task-2-kubernetes` | Kubernetes cluster, networking, and application deployment |
| `task-3-cicd`       | GitLab CI/CD pipeline and DevSecOps automation             |

This allows reviewers to:

* Inspect each task independently
* Review commits specific to a single deliverable
* Trace implementation decisions without unrelated changes
* Compare progress between tasks easily

The final repository combines all completed tasks while preserving the individual development history in their respective branches.

---

# Task Overview

## Task 1 — Bash Scripting

Implemented a robust Bash utility that parses a service inventory file and generates a service health report.

### Key Features

* Input validation
* Colon-separated record parsing
* TCP port validation
* Weight validation
* Environment filtering
* Error handling with stderr/stdout separation
* Safe Bash practices using:

```bash
set -euo pipefail
```

See:

```text
task-1-bash/README.md
```

for complete implementation details and validation examples.

---

## Task 2 — Kubernetes Infrastructure & Application Deployment

Provisioned a self-managed Kubernetes environment using:

| Component    | Technology   |
| ------------ | ------------ |
| Hypervisor   | KVM/libvirt  |
| Provisioning | Vagrant      |
| Kubernetes   | k3s          |
| OS           | Ubuntu 22.04 |

### Deliverables

#### Cluster Bootstrapping

* Control Plane Node
* Worker Node
* Private networking
* API Server access restriction
* Firewall hardening

#### Application Deployment

Two-tier application consisting of:

```text
podinfo
   │
   ▼
 Redis
```

Implemented:

* Namespace isolation
* Secrets management
* Deployments
* Services
* Readiness probes
* Liveness probes
* Resource requests & limits
* Network Policies

#### External Routing

Implemented external access using:

* NGINX Ingress Controller
* Host-based routing
* Ingress resource configuration

A separate write-up compares:

* Ingress API
* Gateway API

and explains why Ingress was selected for this assessment.

#### Monitoring & Observability Recommendation

Proposed production-grade observability stack:

* Prometheus
* Grafana
* Loki
* Promtail
* Node Exporter
* Kube State Metrics

Including:

* Metrics collection
* Logging
* Alerting
* Dashboard strategy

See:

```text
task-2-kubernetes/README.md
```

for full documentation.

---

## Task 3 — DevSecOps CI/CD Pipeline

Designed and implemented a complete GitLab CI/CD pipeline for a Flask + PostgreSQL application.

### Pipeline Stages

```text
Install
   ↓
Test
   ↓
Lint
   ↓
Containerize
   ↓
Scan
   ↓
Push
   ↓
Deploy
```

### Security Controls

* Flake8
* Bandit
* pip-audit
* Trivy

### Containerization

* Multi-container Docker Compose environment
* PostgreSQL backend
* Flask API
* Production Gunicorn server

### Image Delivery

* GitLab Container Registry integration
* Docker image scanning
* Vulnerability remediation workflow

### Deployment Stage

A staging deployment job was implemented that can:

* Update Kubernetes deployments
* Perform rollout validation
* Be connected to a real cluster through GitLab CI variables

### Validation Performed

* Health endpoint testing
* Database connectivity testing
* CRUD validation
* Dependency vulnerability remediation
* Container vulnerability remediation
* Coverage reporting
* Registry publishing

See:

```text
task-3-cicd/README.md
```

for the complete pipeline documentation.

---

# Previous Related Experience

For the monitoring and deployment design decisions in this assessment, I referenced experience from a personal Kubernetes project:

[PricePointScout Project](https://github.com/OmarZakaria10/PricePointScout?utm_source=chatgpt.com)

In that project I implemented:

* Kubernetes deployments
* Helm charts
* Monitoring stacks
* CI/CD automation
* ArgoCD-based GitOps workflows

This practical experience influenced several design choices documented throughout this assessment, particularly around observability and deployment automation.

---
