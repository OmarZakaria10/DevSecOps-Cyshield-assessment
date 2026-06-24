# Monitoring & Observability — Recommendation

> **Scope:** Write-up only. No manifests are created or applied in this repository.

---

## Why This Stack?

I've used this exact combination before — **Prometheus + Grafana + Node Exporter + Kube State Metrics** — in the [PricePointScout](https://github.com/OmarZakaria10/PricePointScout-Helm/tree/main/monitoring-chart) project to monitor a multi-tier Kubernetes application. It proved to be reliable, resource-efficient, and easy to reason about. For this assessment I'd extend that proven foundation with **Loki + Promtail** to cover logs, giving us full-stack observability in a single Grafana UI.

All components would live in a dedicated `monitoring` namespace so they don't pollute the `shop` workload namespace.

---

## The Stack at a Glance

| Tool | Role |
|---|---|
| **Prometheus** | Scrapes, stores, and evaluates metrics (15 s interval, 7-day retention) |
| **Grafana** | Single pane of glass — dashboards + alerting + log explorer |
| **Node Exporter** *(DaemonSet)* | Physical node metrics: CPU, RAM, disk, network |
| **Kube State Metrics** | Kubernetes object health: replica counts, pod phases, resource limits |
| **Loki + Promtail** *(DaemonSet)* | Log shipping and indexing — no heavy agents |

---

## What We'd Scrape

### Cluster-Level — via Kube State Metrics
- `kube_deployment_status_replicas_unavailable` — detects a broken `podinfo` rollout before users notice.
- `kube_pod_container_status_waiting_reason` — catches `CrashLoopBackOff` and `OOMKilled` immediately.
- `kube_pod_container_resource_limits` — validates that resource limits are actually set on every pod.

### Node-Level — via Node Exporter + cAdvisor (built into kubelet)
- CPU saturation (`node_cpu_seconds_total`) and memory pressure (`node_memory_MemAvailable_bytes`) tell us when a bare-metal node is running hot.
- `node_filesystem_free_bytes` warns before disk pressure causes pod evictions.
- cAdvisor's `container_cpu_usage_seconds_total` and `container_memory_working_set_bytes` let us compare actual container consumption against the limits we wrote in the deployment manifests.

### App-Level — podinfo's own `/metrics` endpoint
This is where it gets interesting. `podinfo` already ships a Prometheus-formatted metrics endpoint. We start it on a **separate port** (`9797`) using the `--port-metrics=9797` flag — that's exactly what's configured in `podinfo-deployment.yaml`. This keeps Prometheus scrape traffic completely isolated from real user requests on port `9898`.

Prometheus would scrape it with a `ServiceMonitor` (or a static scrape job) targeting the `podinfo` Service in the `shop` namespace. The most useful metrics here are:

- `http_requests_total` — request throughput broken down by status code.
- `http_request_duration_seconds` — latency histogram; p99 is the one to watch.
- Cache hit/miss counters — indicates whether Redis is doing useful work.

For Redis, we'd add a lightweight **redis_exporter** sidecar to the Redis pod. This surfaces `redis_up`, `redis_connected_clients`, and `redis_memory_used_bytes` — enough to catch most failure modes.

---

## Logs — Loki + Promtail

Promtail runs as a DaemonSet and tails `/var/log/pods` directly from the host. For the `shop` namespace it attaches labels like `{namespace="shop", app="podinfo"}`, making log discovery instant in Grafana.

Because `podinfo` emits **structured JSON logs** (controlled by `--level=info`), we can parse fields inline with LogQL:

```logql
{namespace="shop", app="podinfo"} | json | level="error"
```

This means no regex hacks — just clean, filterable log lines alongside the Prometheus metrics in the same dashboard.

---

## What to Alert On

| Alert | Threshold | Why It Matters |
|---|---|---|
| Pod crash-looping | `restart_count > 3 in 5 min` | Process is dying; needs immediate attention |
| HTTP 5xx error rate | `> 5% over 5 min` | Users are hitting real errors |
| Redis down | `redis_up == 0` | `podinfo` readiness probe will fail; the app goes dark |
| p99 latency spike | `> 500 ms` | Likely Redis saturation or memory pressure |
| Node disk < 10% | Filesystem free ratio | Prevents node-pressure eviction of pods |

Alerts would fire through **Grafana Alerting** (which can reach Slack or email) — no need for a separate Alertmanager on a small bare-metal cluster.
