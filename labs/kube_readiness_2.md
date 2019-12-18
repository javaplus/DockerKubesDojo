
## Fixing the Redis dependency

Even though the application is "not ready", note that it has not actually stopped running.  It's still serving responses to the `/ready` endpoint every time Kubernetes asks.  It will just keep trying forever until it's finally ready.  Let's fix that by deploying a Redis service that our `cloud-native-demo` deployment can resolve.

In the `k8s/redis` directory is a single YAML manifest file with a VERY simple Redis `Deployment` and `Service`.  This is great for local development, but is not a production ready Redis deployment by any means.  Regardless, it shows off a nice feature of Kubernetes Services that we haven't really shown an example of yet.  That feature is the ability to [resolve the ClusterIP of a Service](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#services) by it's logical name.  In other words, you'll be able to resolve the IP address of the Redis instance just by using the name we give to its Kubernetes Service.

Remember that we've configured our application to connect to Redis at the hostname of `redis-test`.  This is visible in `k8s/app-health/deployment.yaml`.

```yaml
        env:
          - name: REDIS_HOST
            value: redis-test
```

This means we should name the Redis Service `redis-test` as well.  Look at how we've named it in `k8s/redis/redis.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    run: redis-test
  name: redis-test
```

It looks like everything is lining up, so lets apply that Redis `Deployment` and `Service` to Kubernetes with the following command:

```bash
kubectl apply -f k8s/redis
```

Watch your dashboard of runnig Pods.  You should see a new `redis-test-***` Pod, and you should also see the `cn-demo-***` Pod reporting a `1/1 READY` status.

```bash
NAME                              READY   STATUS    RESTARTS   AGE
pod/cn-demo-f8bfdc656-cxpjz       1/1     Running   0          19m
pod/redis-test-57f56cb4f8-w9f2v   1/1     Running   0 10s      81
```

Now that the `cn-demo-***` Pod is ready for traffic again, you should be able to navigate to it in your browser again at [http://localhost/](http://localhost/).

## Scale and play with Readiness

Let's manually scale our `Deployment` one more time to see the effect of Readiness Probes when there are more than one replicas in a `Deployment`.

```bash
kubectl scale deployment cn-demo --replicas 3
```

Then let's delete the Redis deployment.  What is your dashboard reporting for the Readiness of the 3 `Pods` that are running in your `Deployment`?  They should all say `0/1 READY` now.  Go ahead and redeploy Redis:

```bash
kubectl apply -f k8s/redis
```

Did they all turn back to ready again?  This is a powerful feature as Kubernetes is watching every Pod in your deployment.  It's also worth reading about [Liveness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).  They have a similar configuration, but will actually restart the container(s) in your `Pod` if they are determined to be unhealthy.  Combining these techniques of Liveness and Readiness will increase the reliability and availability of your system.