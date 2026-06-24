# Task 2 — External Routing (Ingress vs Gateway API)

## Selected Approach: NGINX Ingress Controller

For this assessment, I chose **Option A: NGINX Ingress Controller** to expose the application externally.

The application requirements are relatively simple:

* A single web application (`podinfo`)
* One external hostname
* Basic HTTP routing to a backend service
* No advanced traffic-management requirements

Given these requirements, an Ingress-based solution provides the simplest and most practical implementation while fully satisfying the assessment objectives.

I also have prior hands-on experience operating NGINX Ingress Controller in Kubernetes environments. Since the routing requirements are straightforward, using Ingress allowed me to deliver a reliable and maintainable solution quickly without introducing additional complexity.

---

# Implemented Routing Flow

```text
Client
   |
   v
NGINX Ingress Controller
   |
   v
Ingress Resource
   |
   v
podinfo Service (ClusterIP)
   |
   v
podinfo Pods
```

External traffic enters the cluster through the NGINX Ingress Controller and is routed to the `podinfo` service based on the configured host rule.

Redis remains internal to the cluster and is exposed only through a ClusterIP service.

---

# Why Ingress Was Chosen

## Simplicity

The application only requires exposing a single HTTP service externally.

Ingress provides:

* Host-based routing
* Path-based routing
* TLS support if required
* Straightforward configuration

without requiring additional routing resources.

## Maturity

Ingress is a well-established Kubernetes API that is widely supported across Kubernetes distributions and cloud providers.

The NGINX Ingress Controller is one of the most commonly used ingress implementations and has extensive documentation, community support, and operational maturity.

## Faster Delivery

The assessment does not require advanced routing features such as:

* Canary deployments
* Traffic splitting
* Header-based routing
* Multi-team route ownership

Therefore, introducing Gateway API resources would add complexity without providing significant benefits for this use case.

---

# Ingress API vs Gateway API

Although Ingress was selected for this implementation, it is important to understand the differences between the traditional Ingress API and the newer Gateway API.

## Ingress API

Ingress provides a simple method for exposing HTTP and HTTPS services outside a Kubernetes cluster.

Common capabilities include:

* Host-based routing
* Path-based routing
* TLS termination
* Traffic forwarding to backend services

Example:

```text
Client
   |
Ingress Controller
   |
Service
   |
Pods
```

Ingress works very well for small and medium-sized applications with relatively simple routing requirements.

However, many advanced features require controller-specific annotations, which can reduce portability between implementations.

---

## Gateway API

Gateway API is the next-generation Kubernetes networking API designed to overcome many limitations of Ingress.

Instead of a single routing resource, Gateway API separates responsibilities into multiple resources:

```text
GatewayClass
      |
Gateway
      |
HTTPRoute
```

This design provides better flexibility, ownership separation, and extensibility.

---

# Role Separation

One of the biggest improvements introduced by Gateway API is separation of responsibilities.

### Platform Team Responsibilities

Infrastructure teams typically manage:

* GatewayClass
* Gateway

These resources represent the networking infrastructure and entry points into the cluster.

### Application Team Responsibilities

Application teams manage:

* HTTPRoute
* TCPRoute
* GRPCRoute

These resources define how traffic is routed to their applications.

This separation creates cleaner RBAC boundaries and reduces operational risk in larger organizations.

---

# Expressiveness and Traffic Management

Gateway API provides standardized support for advanced routing features such as:

* Traffic splitting
* Canary deployments
* Blue/Green deployments
* Header-based routing
* Query parameter matching
* Cross-namespace routing

For example, Gateway API can natively split traffic:

```text
90% -> Application Version 1
10% -> Application Version 2
```

In traditional Ingress implementations, these capabilities often depend on vendor-specific annotations.

---

# Protocol Support

Ingress primarily focuses on:

* HTTP
* HTTPS

Gateway API supports additional protocols through dedicated route resources:

* HTTP
* HTTPS
* TCP
* UDP
* TLS
* gRPC

This makes Gateway API suitable for a broader range of workloads.

---

# Why Kubernetes Is Moving Toward Gateway API

Gateway API is becoming the preferred Kubernetes networking model because it provides:

* Better separation of responsibilities
* More expressive routing capabilities
* Improved RBAC boundaries
* Standardized traffic-management features
* Better extensibility
* Multi-protocol support
* Improved portability across implementations

For complex platforms and large-scale Kubernetes environments, Gateway API is generally the recommended direction.

---

# Conclusion

Ingress was selected for this assessment because it is a mature, widely adopted, and operationally simple solution that fully satisfies the project's routing requirements.

For a single application requiring straightforward HTTP exposure, Ingress offers the fastest path to a working solution while remaining easy to maintain and troubleshoot.

If the platform evolved to require advanced traffic management, multi-team ownership, traffic splitting, or more sophisticated routing policies, Gateway API would likely become the preferred choice.
