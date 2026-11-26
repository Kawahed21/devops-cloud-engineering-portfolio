# 03 — Kubernetes Helm Platform

## Objective
Package the sample API as a Helm chart and deploy it consistently to a local Kubernetes cluster or a managed cluster.

## Components
- Deployment with configurable replica count.
- ClusterIP Service.
- Configurable image repository and tag.
- CPU/memory requests and limits.
- Readiness and liveness probes.
- Pod security context and non-root container settings.
- Optional Ingress, disabled by default.

## Prerequisites
- kubectl and Helm 3.
- kind or minikube for local practice, or an existing managed cluster.
- A container image accessible to the cluster.

## Deployment workflow
```bash
kubectl cluster-info
helm lint ./chart
helm template portfolio-api ./chart --values ./chart/values.yaml
helm upgrade --install portfolio-api ./chart --namespace portfolio --create-namespace
kubectl rollout status deployment/portfolio-api -n portfolio
kubectl get pods,svc -n portfolio
```

Use port-forwarding for local access:
```bash
kubectl port-forward svc/portfolio-api 8080:80 -n portfolio
curl -fsS http://localhost:8080/health
```

## Operations to practise
- Scale replicas and observe rollout.
- Change image tag and perform an upgrade.
- Roll back with `helm rollback`.
- Inspect events, logs and resource usage.
- Uninstall the release and remove the namespace when finished.

## Production considerations
Use a dedicated namespace, RBAC, network policies, image pull secrets from a secret manager, Pod Security Standards, disruption budgets and topology spread constraints. Do not put credentials in values files.

## Acceptance criteria
- Helm lint and template render succeed.
- Pods become Ready.
- Service routes traffic to healthy pods.
- Resource requests/limits and probes are configured.
- Upgrade and rollback are demonstrated.

## Next improvements
Add HPA, PDB, NetworkPolicy, cert-manager, External Secrets Operator, Argo CD and policy enforcement with Kyverno or Gatekeeper.
