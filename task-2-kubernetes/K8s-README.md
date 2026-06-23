# Task 2 — Kubernetes: Redis Tier

## Namespace

All resources live in a dedicated `shop` namespace to isolate workloads and avoid touching `default`.

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: shop
```

```bash
kubectl apply -f namespace.yaml
```

---

## Secret (`redis-secret.yaml`)

Credentials are stored in a `Secret` — never hardcoded in the Deployment.  
Two keys are stored:

| Key | Purpose |
|---|---|
| `redis-password` | Passed to `redis-server --requirepass` |
| `cache-server` | Full connection URL consumed by podinfo |

`data` (base64) is used instead of `stringData` (plain text) to make the encoded nature of the values explicit.

```bash
# generate the base64 values
echo -n 'redis123' | base64
echo -n 'tcp://:redis123@redis.shop.svc.cluster.local:6379' | base64
```

```yaml
# redis-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: redis-credentials
  namespace: shop
type: Opaque
data:
  redis-password: cmVkaXMxMjM=
  cache-server: dGNwOi8vOnJlZGlzMTIzQHJlZGlzLnNob3Auc3ZjLmNsdXN0ZXIubG9jYWw6NjM3OQ==
```

```bash
kubectl apply -f redis-secret.yaml
```

---

## Deployment (`redis-deployment.yaml`)

Scaffolded with `--dry-run` then extended:

```bash
kubectl create deployment redis --image=redis:7.2-alpine -n shop \
  --dry-run=client -o yaml > redis-deployment.yaml
```

### Key additions over the generated scaffold

**Password auth via Secret**  
`redis-server` is started with `--requirepass $(REDIS_PASSWORD)`. The env var is injected from the `redis-credentials` Secret — the password never appears in the manifest as plain text.

```yaml
command: ["redis-server", "--requirepass", "$(REDIS_PASSWORD)"]
env:
  - name: REDIS_PASSWORD
    valueFrom:
      secretKeyRef:
        name: redis-credentials
        key: redis-password
```

**Resource requests & limits** (required by the assessment brief)  
Keeps the pod schedulable and prevents it from consuming unbounded memory.

```yaml
resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 250m
    memory: 256Mi
```

**Liveness & readiness probes**  
Both run `redis-cli ping` authenticated with the password to avoid `NOAUTH` errors in logs.  
Liveness restarts a hung process; readiness gates traffic until Redis is ready to serve.

```yaml
livenessProbe:
  exec:
    command: ["sh", "-c", "redis-cli -a \"$REDIS_PASSWORD\" --no-auth-warning ping"]
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  exec:
    command: ["sh", "-c", "redis-cli -a \"$REDIS_PASSWORD\" --no-auth-warning ping"]
  initialDelaySeconds: 2
  periodSeconds: 5
```

```bash
kubectl apply -f redis-deployment.yaml
```

---

## Service (`redis-svc.yaml`)

Exposed as `ClusterIP` (the default) — reachable only from within the cluster.  
No `NodePort` or `LoadBalancer` is set, so Redis is never accessible externally.

```bash
kubectl expose deployment redis -n shop \
  --type=ClusterIP --port=6379 \
  --dry-run=client -o yaml > redis-svc.yaml
```

```yaml
# redis-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: shop
spec:
  selector:
    app: redis
  ports:
    - port: 6379
      targetPort: 6379
```

podinfo references Redis via the stable in-cluster DNS name: `redis.shop.svc.cluster.local:6379`.

```bash
kubectl apply -f redis-svc.yaml
```

---
