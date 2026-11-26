# Kubernetes Helm Platform

The chart in `chart/` deploys the FastAPI service with a ClusterIP Service, configurable replicas/image, HTTP readiness/liveness probes, resource requests/limits and pod hardening (non-root UID, seccomp RuntimeDefault, read-only root filesystem, dropped capabilities and no service-account token mount).

## Validate
```bash
helm lint chart
helm template portfolio-api chart --values chart/values.yaml
```

## Deploy to a disposable cluster
Build and publish the API image first, then override the image repository and immutable tag:
```bash
kubectl create namespace portfolio --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install portfolio-api chart --namespace portfolio \
  --set image.repository=YOUR_REGISTRY/portfolio-api --set image.tag=YOUR_TAG
kubectl rollout status deployment/portfolio-api -n portfolio
kubectl port-forward svc/portfolio-api 8080:80 -n portfolio
curl -fsS http://127.0.0.1:8080/health
```

Uninstall with `helm uninstall portfolio-api -n portfolio`. Add NetworkPolicy, PDB, HPA, topology spread constraints, digest pinning and TLS ingress for a production deployment.
