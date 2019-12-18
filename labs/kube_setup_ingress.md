
# ~~ Ingress ~~

As mentioned before, the `Service` we exposed to our Pods is a ClusterIP, and only visible within the cluster.  To get to it, we had to do a port forwarding technique.  In a Test or Production environment, we would probably like to have a stable DNS name to be able to access our service.  This is what Kubernetes `Ingress` provides.  Your cluster Operators will likely host one or a few Ingress endpoints from which you can define your own `Ingress` definitions.  With your local Kubernetes environment in Docker Desktop, you can also run an Ingress Controller.  You'll get the behavior of an Ingress Controller, minus an actual Load Balancer infront of it like you would find in a production scale cluster.

## Deploy the Nginx Ingress Controller

To start, deploy the Nginx Ingress Controller to your local Kubernetes instance with the following commands:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud-generic.yaml
```

It might take a few minutes, but when finished you should have a new namespace called `ingress-nginx` with a single `Pod` running in it which is the Ingress Controller.  Let's run some commands locally to see the effect when it's all complete.  Note the new namespace and how the `-n` switch can be used to query for `Pods` and `Services` in that namespace instead of the default we've used so far.  Also note the `LoadBalancer` type given to the `ingress-nginx` Service.  So far we've only used ClusterIP.  `LoadBalancer` type in a cloud environment creates a real Load Balancer "of the cloud".  An AWS ALB load balancer for example.  Docker Desktop has a convenient feature where it listens on `localhost` when you create Services of type `LoadBalancer`.

> NOTE:  Even in production, you'll likely use ClusterIP Service types a majority of the time and use the Operator provided Ingress to get HTTP traffic to your services.

```
> kubectl get ns
NAME              STATUS   AGE
default           Active   37h
docker            Active   36h
ingress-nginx     Active   35h
kube-node-lease   Active   37h
kube-public       Active   37h
kube-system       Active   37h

> kubectl -n ingress-nginx get pod,service
NAME                                            READY   STATUS    RESTARTS   AGE
pod/nginx-ingress-controller-7dcc95dfbf-4mwqf   1/1     Running   2          35h

NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/ingress-nginx   LoadBalancer   10.100.245.43   localhost     80:31696/TCP,443:31067/TCP   35h
```

If all has gone well up until now, you should be able to navigate to [http://localhost:80](http://localhost:80) in your browser and see a `404 Not Found` response come back.  This is the default `404` page being served up by the Nginx Ingress Controller, because we haven't defined any `Ingress` configurations yet.

## Clean-up

Before we proceed, let's clean up the `Deployment` from the last section.  We will `kubectl delete` the same config file we used for `kubectl apply`.

```bash
kubectl delete -f k8s/app-envvars/deployment-base.yaml
```

## Apply the Deployment, Service and Ingress

Are you liking declarative Infrastructure as Code yet?  Full environments can come and go with ease, and we about to stand up a few things all in one shot.  A working `Deployment`, `Service` and `Ingress` are ready for you in the `k8s/app-ingress` directory.  Rather than `kubectl apply` these YAML files one by one, we're going to do them all at once just by applying the entire directory.

```bash
kubectl apply -f k8s/app-ingress
```

We skipped over the creation of `Ingress` and `Service`, but it's more important to look at their configuration to see how they relate rather than try to memorize YAML configurations.  Open their configurations in the `k8s/app-ingress` directory and try to follow the connections from Ingress, to Service, to Pod.

```
http request --> Ingress --> Service --> Pod(s)
```

Ingress forwards to a named Service on a Port, the Service then forwards to one or more Pods based on label selectors.  If you're wondering how our Pods ended up with a label selector of `run: cn-demo`, check the `deployment.yaml`.

With all of this applied, we should be able to access our application by going to [http://localhost:80](http://localhost:80).  This time, instead of a `404` page, we should see our familiar JSON response with all our application configuration showing.  Note too that we don't have to do the `kubectl port-forward` command anymore.  We're coming in the front door of our local Kubernetes instance via `localhost` because we've set up an Ingress Controller there.
