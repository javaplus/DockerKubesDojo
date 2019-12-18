Your team loves you so much they also created a small **tools** Docker image with handy CLI tooling to help visualize and troubleshoot what's going on in your local Kubernetes namespace.  It's a great way to share tools amongst the team, so you decide to start it up.  The Docker image they gave you has the `watch` and `kubectl` commands, which you're about to see are a handy way to keep tabs on what Pods or other services are configured and running in your namespace.

The tools Docker image does not contain authentication tokens to connect to your local Kubernetes cluster (everyone has their own), so we'll mount those from your local machine into the running tools container so they're available to `kubectl`.  We're mounting into the default location as well so we don't need to configure anything additional

> Note the `-it` and `bash` in this CLI statement.  These say "run the bash CLI interpreter in interactive mode" which will give us a bash prompt once the container is running.

> Note: In the following command, replace `<username>` with the path to your own local user directory.  If executing in Git Bash (mintty) you will need to include `winpty` at the beginning of the command.

**Windows**
```bash
docker run --rm -it -v C:\Users\<username>\.kube\:/root/.kube CHANGEME/cloud-native-demo-tools bash
```

**MacOS/Linux**
```bash
docker run --rm -it -v $HOME/.kube/:/root/.kube CHANGEME/cloud-native-demo-tools bash
```

Once you see a `bash` prompt, type the following command.  You're technically on a Linux bash prompt at this point, so the next command is the same for all desktop platforms.

```bash
watch -n 1 kubectl get all,endpoints,ingress
```

You now have a text-based dashboard updating every 1 second of your namespace showing Pods, Deployments, Services, Endpoints and Ingress.  You can type `CTRL+C` to exit this dashboard and then `CTRL+D` to exit out of the container (which also terminates this particular container), but lets keep it running for now.