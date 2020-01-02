# ~~ Infrastructure as Code ~~

While the above `kubectl ...` CLI commands are useful for your Developer Inner Loop, when it comes time to deploy to Test and Production environments you want something a little more repeatable.  We want the declarative configuration of the `Deployment` we were just exploring in a text based format that we can store alongside our application code in Git.  Using `kubectl` again, we can query that configuration back out of the Kubernetes cluster.

It's a good time to point out that `kubectl` is just a friendly CLI that gives us convenient access to the Kubernets API Server.  When we add or change configuration to Kubernetes with commands like `kubectl run ...`, there are PUT/POST calls being issued to the Kubernetes API Server.  Likewise, once configured, we can retrieve the configuration with an HTTP GET, or `kubectl get ...`.

So there's a lot of good configuration already in our cluster for the `Deployment` we have.  It'd be a shame to lose it, so let's get it out and store it in a file.

> Note: Up to now, it didn't matter which directory you were running kubectl commands from, since we were just getting details on our Kubernetes environment, or else communicating directly between docker and the cluster.  From here on out we will be using YAML files (included in this repository) to describe the deployment, and so you will need to execute these commands from your root project directory.

## Get the Configuration for your Deployment

```bash
kubectl get deployment cn-demo -o yaml > k8s/lab/deployment.yaml
```

That command semantically says "get me the configuration of the Deployment named cn-demo, format it as YAML and write it to the file k8s/lab/deployment.yaml".  Go ahead and open that file in VS Code and look around.  Do you see the familiar values you defined with the `kubectl` CLI earlier for the `cloud-native-demo:1` image and the `replicas` count?  There's a lot of other data in there too, some relevant, some not.

Using `kubectl get ...` is a common technique to bootstrap your configuration without needing to remember all the structure of the YAML document, which in turn is really just the API specification for Kubernetes Deployments.  We're going to use a cleaned up version of `deployment.yaml` for our next steps, but just remember how to use `kubectl get ... -oyaml` in the future.  You'll use it often to troubleshoot your Kubernetes configuration.

> Note: In this example we **piped** the results of `kubectl get ...` to a file using the `>` character.  If you leave that part off, the results will be written to your console.  You'll do this often when you just need to see the configuration of a particular Kubernetes object.

Before we continue, let's clean up our current deployment.  Going forward, we'll work with and deploy using variations of `deployment.yaml` contained in this repository.

```bash
kubectl delete deployment cn-demo
```
