
# ~~ Detecting an unhealthy app ~~

Let's try the `/counter` URL endpoint of our application by going to [http://localhost/counter](http://localhost/counter) in our browser.  You should see the following.

```json
{
    "error": "service unavailable"
}
```

That's accurate, but not what we want.  We have an unhealthy application that can't find it's backing service (Redis in this case).  What if I had a deployment with 3 replicas and one of them could not establish the connection to Redis.  I would want Kubernetes to stop routing traffic to that unhealthy application until it became healthy again.  The definition of "health" will vary from app to app, and this is why Kubernetes allows you to write this logic yourself.  There are various techniques, but our implementation exposes a single `/health` URL endpoint that returns a `200 OK` response if healthy, and a `503` if not.

We need to configure Kubernetes to periodically call this endpoint, and remove the Pod as a valid endpoint in my `Service` if it is unhealthy.  This is exactly what the `readinessProbe` feature is meant to do.  In this case, it's configured for you in `k8s/app-health/deployment.yaml`.  Look for the following section which configures the `readinessProbe`.  Details on what all these values mean can be [found here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes).

```yaml
        readinessProbe:
          timeoutSeconds: 1
          periodSeconds: 1
          initialDelaySeconds: 1
          httpGet:
            path: /ready
            port: 5000
```

## Spotting unhealthy Pods

We're going to apply this new `Deployment` with the `readinessProbe` configured, but lets look at our current Pod before we do.  In our console based dashboard, you should see a single Pod running with output like the following:

```bash
NAME                       READY   STATUS    RESTARTS   AGE
cn-demo-7bbddfb4bf-g4rlk   1/1     Running   0          3m
```

The callout here is the `1/1 READY` section.  This is Kubernetes saying "I should have 1 Pod ready, and 1 is reporting as ready".  This is not the case though as the Redis dependency is missing.  Let's apply the new `Deployment` and observe the change.

```bash
kubectl apply -f k8s/app-health
```

The configuration changed so Kubernetes will Terminate the old Pod and create a new one in its place.  Check the Pod status this time though.

```
NAME                      READY   STATUS    RESTARTS   AGE
cn-demo-f8bfdc656-8jz57   0/1     Running   0          13s
```

It's stuck in `0/1 READY` because the newly added `readinessProbe` is failing.  Let's see the effect it had on the application in the browser.  Navigate one more time to [http://localhost/](http://localhost/).  Not even a `404 Not Found` this time, instead we're getting a `503` error from the Nginx Ingress Controller telling us there are no ready Pods to service the request.
