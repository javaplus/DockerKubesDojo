Your team loves you so much they also created a small **tools** Docker image with handy CLI tooling to help visualize and troubleshoot what's going on in your local Kubernetes namespace.  It's a great way to share tools amongst the team, so you decide to start it up.  The Docker image they gave you has the `watch` and `kubectl` commands, which you're about to see are a handy way to keep tabs on what Pods or other services are configured and running in your namespace.

The tools Docker image does not contain authentication tokens to connect to your local Kubernetes cluster (everyone has their own), so we'll mount those from your local machine into the running tools container so they're available to `kubectl`.  We're mounting into the default location as well so we don't need to configure anything additional

> Note the `-it` and `bash` in this CLI statement.  These say "run the bash CLI interpreter in interactive mode" which will give us a bash prompt once the container is running.

> Note: In the following command, replace `<username>` with the path to your own local user directory.  If executing in Git Bash (mintty) you will need to include `winpty` at the beginning of the command.

**Windows**
```bash
docker run --rm -it -v C:\Users\<username>\.kube\:/root/.kube javaplus/kube-demo-tools bash
```

**MacOS/Linux**
```bash
docker run --rm -it -v $HOME/.kube/:/root/.kube javaplus/kube-demo-tools bash
```

You should eventually see a `bash` prompt which means you're running `bash`, in a Container, on a Linux Operating System (a virtualized Linux OS if you're on Windows or MacOS).  Next, run the `kubectl` command to validate our authentication tokens were mounted into the container correctly.

```bash
kubectl get all,endpoints,ingress
```

You should see output similar to the following:

```
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   45d

NAME                   ENDPOINTS           AGE
endpoints/kubernetes   192.168.65.3:6443   45d
```

Next let's play with `watch`.  `watch` is simply a command that repeatedly runs another command on some interval.  Let's test it by running `watch date`.  `date` is the command we want to run over and over, and should just report the current date and time.

```bash
watch date
```

You should see the current date and time updated every 2 seconds.

```bash
Every 2.0s: date                             2019-12-27 16:32:25

Fri Dec 27 16:32:25 UTC 2019
```

When you combine `watch` and `kubectl`, you can get a handy console based dashboard of the current state of your Kubernetes Namespace.  Run the following command, where we also include `-n 1` which will cause `watch` to rerun the `kubectl` command every 1 second instead of the default 2 seconds.

```bash
watch -n 1 kubectl get all,endpoints,ingress
```

You now have a text-based dashboard updating every 1 second of your namespace showing Pods, Deployments, Services, Endpoints and Ingress.  You can type `CTRL+C` to exit this dashboard and then `CTRL+D` to exit out of the container (which also terminates this particular container), but lets keep it running for now.
