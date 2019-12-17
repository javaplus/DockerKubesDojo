# Docker and Kubernetes Dojo
Tutorial on Using Docker and Kubernetes

**Big thanks to [Michael Frayer](https://github.com/frayer) for most of the content of this tutorial is from him!** 


## Pre-requisites:

Generally speaking you need to have the Git client and Docker along with Kubernetes installed locally.

#### A console or shell environment

Some basic skills working with command line tooling are required to complete this tutorial as you will interact with the CLI often throughout.  Windows Command prompt or Powershell is recommended for Window's users.  MacOS and Linux users can use their shell of choice.  It will be called out where there is a difference in CLI statements for Windows vs MacOS/Linux users.


#### Git
If you don't already have a Git Client, you can download the Git tools from here:
 - https://git-scm.com/downloads
 

#### Docker & Kubernetes:

Here are links and instructions per operating system:


##### Windows
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 15063 or later)
    - Docker Desktop Download which Includes Kubernetes: https://www.docker.com/products/docker-desktop
    - Docker Desktop Install Guide - https://docs.docker.com/docker-for-windows/install/
    - Enable Kubernetes 
    
- Older Windows Versions:
  - Docker Toolbox:  https://docs.docker.com/toolbox/toolbox_install_windows/
  - Kubernetes Support via Minikube(Click on the *Windows* tab under each section): https://kubernetes.io/docs/tasks/tools/install-minikube/ 
  - Blog on working with Minikube on Windows: https://rominirani.com/tutorial-getting-started-with-kubernetes-on-your-windows-laptop-with-minikube-3269b54a226
  
##### Mac
  - Docker Desktop for Mac : https://hub.docker.com/editions/community/docker-ce-desktop-mac

#### Optional Pre-reqs (For both Mac and Windows)
##### Install Visual Studio Code

You will be editing YAML files and viewing Python code during the course of this exercise.  You can use any text editor, but Visual Studio Code is recommended.

[Download and install VS Code](https://code.visualstudio.com/)


##### Install the JSON Formatter Chrome Extension

This is a useful, but not required, Chrome extension for viewing JSON output in your browser.

[Install using a Chrome browser](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa)
  

---

# ~~ Getting started ~~

You and your team are on a mission to begin rearchitecting your monolithic application towards a micro-service based architecture.  While your team has some experience working with Containers, they've asked for your help in realizing the full potential of Cloud Native patterns when it comes to the design and operational concerns of your new architecture.  You did your homework on [12-factor apps](https://12factor.net/) and the feature set of [Kubernetes](https://kubernetes.io/docs/concepts/) and have given your team a set of requirements to produce a first cut of a microservice which will serve as the foundational codebase for all your microservices.

The features you've asked for in this foundational application include:

* It follows the 12-factor Application [Configuration](https://12factor.net/config) principle.  Environmental configuration in this application will be read from Environment Variables.
* It follows the 12-factor Application [Stateless Process](https://12factor.net/processes) principle.  It is completely stateless and scales horizontally.
* All dependencies are declared and ship with the application as an OCI compatible image.
* The application supports Infrastructure as Code principles to enable a Continuous Delivery pipeline.
* The application must expose information about its health in order for Kubernetes to know it's running and can accept traffic.

And the team has delivered.  They have created an [OCI compatible image](https://www.opencontainers.org/) and have already loaded it into the [Docker Trusted Registry](Change ME!).  They've given you the following information on how it behaves and the default URL endpoints it exposes.

* It's a Python application with a dependency on a Redis instance.  The application is configurable through command line switches and the documentation for them can be found by running `python app.py --help`.
* When running, it listens for HTTP connections on port `5000` by default.  This is configurable.
* The following URL endpoints are available:
  * `/`
    * Returns a JSON message with information about the application and its configuration.
  * `/counter`
    * Returns a count of how many times the `/counter` URL has been accessed for this particular application.  The key for the count is the `HOSTNAME` environment variable for the running application.
  * `/counter/reset`
    * Resets the counter being returned in `/counter` to `0`.
  * `/live`
    * Returns a `200` HTTP status code if the application is running.  Useful for a [Kubernetes liveness probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
  * `/live/{delay}}`
    * Introduces a `delay` for the HTTP response of the `/live` endpoint in seconds.  The team left this in for you to validate your liveness probes are configured correctly for when this endpoint doesn't respond in a timely manner (which could indicate the service is not live anymore).
  * `/ready`
    * Similar to the `/live` endpoint, but this one goes the extra mile and makes sure the service has a healthy connection to the backing Redis service.  This is useful for [Kubernetes readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) which will not send network traffic to the service until it indicates its ready.

You're ready to kick the tires on this service to get a feel for it, with an end goal of creating the Kubernetes manifests that can host the appliation.  The manifests, in YAML format, will live alongside this codebase and augment the foundational codebase with the foundational Configuration as Code to run it in any Kubernetes cluster.

* Deploy with `kubectl run`
* port-forward to consume
* Note how that if you delete the Pod it comes right back
* Scale the deployment from the command line
* Capture the resulting deployment with `kubectl get` and store to file
* Delete existing deployment and modify the declarative Deployment to have an initial replica count of 3
* Modify deployment to set environment variables
* Define a Service and Ingress
* Try to hit an endpoint which interacts with Redis (should error since redis isn't running)
* Deploy a single node Redis and expose it at a service with `kubectl`
* Configure liveness and readiness probes

---

# ~~ Set up your local workspace ~~

## Clone this repository

You'll be working with this repository and configuration contanied within.  Clone it to a location of your choosing and open the directory in VS Code.

> TIP: Run the following command from a directory containing no paths.  On Windows, a root directory of `C:\devl\ws` is a good convention.  In MacOS or Linux, this author uses a convention of `$HOME/code`.

```bash
git clone https://github.com/javaplus/DockerKubesDojo.git
```

---

# ~~ Running locally with Docker Desktop ~~

Before you even think about running this in Kubernetes, you want to run a single instance of it using your local Docker Desktop instance.  While a Kuberentes cluster will ultimately run your application container reliably at scale, it all starts with knowing how to run a single instance using the Docker runtime.

## Run the cloud-native-demo image and expose its port

> HINT: The string CHANGEME `cloud-native-demo:1` captures the coordinates of the Docker/OCI image.  It follows the pattern `{hostname to retrieve image}/{repository name}/{image name}:{tag}`.

> HINT: The `--rm` just cleans up any remaining bits after this application runs.  It's completely stateless, so we don't need to remember anything about its execution in this scenario.

> HINT: The `-p` switch exposes the port the container listens on to your localhost interface.

```bash
docker run --rm -it -p 5000:5000 CHANGEME/cloud-native-demo:1
```

## Validate the application container is running

In your browser, navigate to the URL [http://localhost:5000](http://localhost:5000).  You should see a JSON response with some information about the running application.  If not, double check the `docker run ...` command you issued and look for any errors in the console output.

## Stop the container

In the original CLI window where you issued the `docker run ...` command, type `CTRL+C` to stop the container.

---

# ~~ Running in your local Kubernetes cluster ~~

Now that you know how to run a single instance, it's time to try the same in Kubernetes.  Kubernetes can orchestrate and schedule your container workloads in very flexible ways, but at the end of the day it's going to invoke a Docker or other [CRI compatible runtime](https://www.opencontainers.org/) to run your application in a similar manner as we just did.  Accomplishing this task will get us on our way towards completing our goals (what are our goals).

## Kubernetes text based dashboard

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


## Run the cloud-native-demo image in Kubernetes

Next we want to run the **real** application in Kubernetes and not just this **tools** image.  Open up a new Powershell or Bash window depending on your platform so we don't lose the console based dashboard we have running.

**In a new console window** run the following to run the `cloud-native-demo` image as a container in Kubernetes:

```bash
kubectl run cn-demo --image=CHANGEME/cloud-native-demo:1
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

You deleted **that** specific Pod, but then another one with a new name showed up in its place.  That Pod is running the exact same container, and something extra in the Kubernetes cluster is making sure at least 1 of your Pods is running.  That **extra something** is called a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), and it is always working to ensure the number of Pods running for a given `Deployment` match its configured `replica` count.  The `kubectl run ...` command you just ran created a `Deployment` for you even though you didn't ask for one.  In fact, you should see it in your dashboard named `cn-demo`, happily reporting that `1/1` or "1 of 1" Pods are currently available.

If you're thinking "a Deployment must be involved in how Horizontal Scaling works", you'd be right.  Let's attempt that next.

```bash
kubectl scale deployment cn-demo --replicas 3
```

Check your dashboard again.  Do you see 3 Pods for `cn-demo-***` running?  Your `Deployment` should report `3/3` after some time as well.

Try some other scenarios to see how Kubernetes behaves:
* Delete one of the newly created `Pods` with `kubectl delete ...`
* Scale the `Deployment` in and out, using different numbers for `--replicas`
* Do you notice anything interesting with which Pods Kubernetes decides to keep when you scale in?  Look at the time the Pod has been running.

---

# ~~ Infrastructure as Code ~~

While the above `kubectl ...` CLI commands are useful for your Developer Inner Loop, when it comes time to deploy to Test and Production environments you want something a little more repeatable.  We want the declarative configuration of the `Deployment` we were just exploring in a text based format that we can store alongside our application code in Git.  Using `kubectl` again, we can query that configuration back out of the Kubernetes cluster.

It's a good time to point out that `kubectl` is just a friendly CLI that gives us convenient access to the Kubernets API Server.  When we add or change configuration to Kubernetes with commands like `kubectl run ...`, there are PUT/POST calls being issued to the Kubernetes API Server.  Likewise, once configured, we can retrieve the configuration with an HTTP GET, or `kubectl get ...`.

So there's a lot of good configuration already in our cluster for the `Deployment` we have.  It'd be a shame to lose it, so let's get it out and store it in a file.

> Note: Up to now, it didn't matter which directory you were running kubectl commands from, since we were just getting details on our Kubernetes environment, or else communicating directly between docker and the cluster.  From here on out we will be using YAML files (included in this repository) to describe the deployment, and so you will need to execute these commands from your root project directory.

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

---

# ~~ Environment Variables ~~

## Redeploy the baseline

One of your original asks was that this application be configurable via Environment Variables.  We're now going to put that to the test.  Our first steps will be to redeploy the application, now using the declarative YAML in the `k8s/app-01` directory of this project.  To do that, we're going to use the `kubectl apply ...` command.

```bash
kubectl apply -f k8s/app-envvars/deployment-base.yaml
```

If you check your dashboard, you should see a single Pod running again.  Go ahead and take a look at the `k8s/app-envvars/deployment-base.yaml` file to get familiar with it.  It's a slimmed down version of the `Deployment` YAML you got in the previous step with `kubectl get ... -oyaml`.

## Connect to the Container

We never actually tested the application in the last step, but lets do that now by exposing the `Pod` as a `Service` and using the `kubectl port-forward` command to connect to it.  A Kubernetes `Service` is a lengthy topic, and more can be [read here](https://kubernetes.io/docs/concepts/services-networking/service/).  We'll be focusing on creating what's known as a ClusterIP Service, which means there will be a single addressable endpoint available in the cluster to access the Pod(s) hosting our application.  First thing is first, let's expose the `Service` using `kubectl expose ...`.

```bash
kubectl expose deployment cn-demo --port 5000 --target-port 5000
```

This command says "Create a new ClusterIP Service that listens on port 5000 and targets port 5000 of all Pods that are a part of the cn-demo Deployment".  Next lets connect to this newly created `Service`.  The `kubectl port-forward` command will expose a port on our local machine that connects to ports exposed on Pods.  We need to do the `port-forward` command here because the Pod is only accessible inside the cluster right now.  

```bash
kubectl port-forward svc/cn-demo 5000
```

> Earlier we said that port-forward connects to a Pod, but here we're port forwarding to a Service.  What???  In this case, think of the Service as an alias to one to many Pods that it load balances across.  It's a kubectl trick, but just a single Pod will be selected for forwarding, even if there are many replicas of it.

At this point we should be able to access [http://localhost:5000](http://localhost:5000) from our browser.  Give it a try.  You should see the familiar JSON output we saw earlier when running the container with Docker.  Your value for `host` will vary.

```json
{
  "appName": "cloud-native-demo",
  "env": {
    "host": "cn-demo-7df548dcf8-wpr8v",
    "user_defined_1": null,
    "user_defined_2": null,
    "user_defined_3": null
  },
  "redis-host": "localhost",
  "version": "1.0.0"
}
```

Once you're finished, stop the port forwarding command by pressing `CTRL+C`.

## Configure the User Defined variables

> TIP: The completed deployment configuration is in the `k8s/app-envvars/deployment-with-envvars.yaml` file if you need help through this section.

Right now we have a lot of `null` values for the `user_defined_#` variables.  Let's fix that.  In the `k8s/app-envvars/deployment-base.yaml` file, find the section that looks like the following:

```yaml
      containers:
      - image: CHANGEME/cloud-native-demo:1
        imagePullPolicy: IfNotPresent
        name: cn-demo
```

Add a new section directly under `name: cn-demo` with the following.  Indentation matters here.

```yaml
        env:
          - name: USER_DEFINED_1
            value: my-user-define-value-1
```

With just this configuration, re-apply this `Deployment`.  Kubernetes will see the difference in configuration and redeploy a new `Pod` with the updated configuration.  The old `Pod` will be terminated as it no longer matches the desired state of your deployment (it doesn't have the right configuration anymore).  Assuming you didn't change the filename, run the following and watch your dashboard for how the old and new `Pods` cycle.

```bash
kubectl apply -f k8s/app-envvars/deployment-base.yaml
```

Finally, run the same `port-forward` command you ran earlier and try to access the application in your browser at [http://localhost:5000](http://localhost:5000).  Do you see the updated value for `user_defined_1`?  If you look at the application code in the `app.py` file at the root of the repo you cloned, you can see how the Python code is reading from an Environment Variable to populate that section of the JSON response.

> NOTE: Be very careful in a production system with your environment configuration.  It's useful for this demo to return environment variables off one of the API endpoints.  A production system though will sometimes hold sensitive information in environment variables.  Would you want someone seeing your database connection string after calling a URL like this?  Nope!

## Fill in the remaining environment variables

Using the same pattern as above, fill in the following environment key-value pairs as environment variables and observe the changes in the running application after redeploying.

```bash
USER_DEFINED_2=my-user-define-value-2
USER_DEFINED_3=my-user-define-value-3
REDIS_HOST=redis-test
REDIS_PORT="6379"
```

## Pass the REDIS_HOST env var as a CLI argument to the application

While our application has the ability to read directly from the configured Environment Variables, some applications are configured via CLI arguments on startup.  So far, we haven't actually told Docker or Kubernetes which Python script to run at startup.  It's been using the default `CMD` instruction defined in the original `Dockerfile` it was built from.  You can see in the `Dockerfile` in this repository, it's running the command `python app.py` by default.

This program actually accepts a few configuration values on the CLI.  Our always helpful development team left a `--help` argument in there to help discover what some of them are.  Let's run that now in a new container using Docker.  It only needs to run long enough to give us the output.  In a new console window, run the following:

```bash
docker run --rm CHANGEME/cloud-native-demo:1 python app.py --help
```

You should see the following output:

```bash
docker run --rm cloud-native-demo:1 python app.py --help

usage: app.py [-h] [--port PORT] [--host HOST] [--redis-host REDIS_HOST]
              [--redis-port REDIS_PORT]

Starter Python + Redis app

optional arguments:
  -h, --help            show this help message and exit
  --port PORT, -p PORT  port number to listen for HTTP requests
  --host HOST           host to bind to
  --redis-host REDIS_HOST
                        hostname of the backing Redis service
  --redis-port REDIS_PORT
                        port number of the backing Redis service
```

Soon, we're going to deploy an instance of Redis into the cluster to connect to.  Let's pass the `REDIS_HOST` environment variable we configured in the last step as a CLI argument to the Python application so we can control the Redis host the application connects to.

You can override the start command (right now it's defaulting to what was defined in the Dockerfile) using the `command` property in your `Deployment` YAML.  The `command` property goes at the same depth the `env` property did in the last step.  Add the following to your `Deployment` and try to redeploy it with the `kubectl apply -f ...` command used before.  Take note of how `REDIS_HOST` is passed, surrounded by `$()`.  This is important for the variable to resolve at runtime, otherwise it would just take the literal string `$REDIS_HOST`.

> Use the completed `deployment-with-envvars.yaml` file as a guide if you're having trouble placing this configuration in the file.

```yaml
        command:
          - sh
          - -c
          - |
            python app.py --redis-host $(REDIS_HOST)
```

We will test that this is working correctly in a bit, but first let's set up `Ingress` and a `Service` to make testing our application via a browser a little easier going forward.

---

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

---

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

# ~~ Conclusion ~~

This exercise has introduced you to some of the most commonly used features of Kubernetes for configuring and hosting applications using declarative, Infrastructure as Code techniques.  Even what we've shown here only begins to scratch the surface.  Here are other topics you'll want to dig deeper on as you continue your Kubernetes journey.

* [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/)
* [Declaring and using ConfigMaps to configure a Deployment](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
* [Declaring and using Secrets to configure a Deployment](https://kubernetes.io/docs/concepts/configuration/secret/)
