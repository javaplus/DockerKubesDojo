# ~~ Running in your local Kubernetes cluster ~~

Now that you know how to run a single instance, it's time to try the same in Kubernetes.  Kubernetes can orchestrate and schedule your container workloads in very flexible ways, but at the end of the day it's going to invoke a Docker or other [CRI compatible runtime](https://www.opencontainers.org/) to run your application in a similar manner as we just did.  Accomplishing this task will get us on our way towards completing our goals (what are our goals).

## Run the cloud-native-demo image in Kubernetes

Next we want to run our application in Kubernetes.  Open up a new Powershell or Bash window depending on your platform so we don't lose the console based dashboard we have running.

**In a new console window** run the following to run the `cloud-native-demo` image as a container in Kubernetes:

```bash
kubectl run cn-demo --image=cloud-native-demo:1
```

Watch your console based dashboard.  You should see a Pod that starts with the name `cn-demo-` show up.  Behind the scenes, Kubernetes is retrieving the image and executing it using Docker (in the case of the Kubernetes instance provided by Docker Desktop).  If all goes well, you should eventually see that the Pod is up and running with output in the dashboard similar to the following:

```bash
NAME                           READY   STATUS    RESTARTS   AGE
pod/cn-demo-759dc65498-j2mm6   1/1     Running   0          22s
```

## Play with the new Deployment

It's time to explore some behavior and terminology of Kubernetes.  First up is the [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod/).  We wont' go too deep on all the specifics, but a Pod is where the configuration for your running container resides.  It turns out you can run multiple containers in a single Pod, but that is outside the scope of this exercise.  To learn more about how and why you would want to do this, search around for Sidecar and Ambassador patterns.

Let's see what happens when we delete a Pod (which is one way to brute force simulate a failed container).  Run the following command, filling in the `cn-demo-***` with the unique name Kubernetes assigned your Pod, and keep an eye on your dashboard at the same time.  Things will happen fast!

```bash
kubectl delete pod cn-demo-***
```

You deleted **that** specific Pod, but then another one with a new name showed up in its place.  That Pod is running the exact same image, and something extra in the Kubernetes cluster is making sure at least 1 of your Pods is running.  That **extra something** is called a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), and it is always working to ensure the number of Pods running for a given `Deployment` match its configured `replica` count.  The `kubectl run ...` command you just ran created a `Deployment` for you even though you didn't ask for one.  In fact, you should see it in your dashboard named `cn-demo`, happily reporting that `1/1` or "1 of 1" Pods are currently available.

If you're thinking "a Deployment must be involved in how Horizontal Scaling works", you'd be right.  Let's attempt that next.

```bash
kubectl scale deployment cn-demo --replicas 3
```

Check your dashboard again.  Do you see 3 Pods for `cn-demo-***` running?  Your `Deployment` should report `3/3` after some time as well.

Try some other scenarios to see how Kubernetes behaves:
* Delete one of the newly created `Pods` with `kubectl delete ...`
* Scale the `Deployment` in and out, using different numbers for `--replicas`
* Do you notice anything interesting with which Pods Kubernetes decides to keep when you scale in?  Look at the time the Pod has been running.
