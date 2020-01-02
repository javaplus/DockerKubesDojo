# ~~ The Mission ~~

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

---

### Build and run the cloud native app

Before you even think about running this in Kubernetes, you want to run a single instance of it using your local Docker Desktop instance.  While a Kuberentes cluster will ultimately run your application container reliably at scale, it all starts with knowing how to build and run a single container using the Docker runtime.

### Get the Code

We've provided the source code and Dockerfile to build the image in this repo.

Clone this repo. https://github.com/javaplus/DockerKubesDojo.git

After cloning the repo locally, open a command prompt to the root of the project where the Dockerfile resides.

Look at the Dockerfile:

```
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

LABEL org.opencontainers.image.title="cloud-native-demo"

COPY . .

CMD [ "python", "./app.py" ]
```

This docker file simply starts with a pre-existing image that has python installed and then copies the local source code and requirements to the image and states that the command to run when the container starts is "python ./app.py".  That is start the python app.

These are the instructions that tell docker how to build this image.  We will now use this file to create a Docker image with our app.

Run the docker build command like this:

```

docker build -t cloud-native-demo:1 .

```

The -t tells Docker to tag this image with the name "cloud-native-demo" and create version "1".  The '.' at the very end tell docker where to find the Dockerfile.  In our case, this is the current directory, thus the '.'.

You should see something like this(NOTE: the output below is abbreviated):

```
D:\workspaces\DockerKubesDojo>docker build -t cloud-native-demo:1 .
Sending build context to Docker daemon  118.3kB
Step 1/7 : FROM python:3
3: Pulling from library/python
8f0fdd3eaac0: Pull complete
...
644b4ceca849: Pull complete
50f0ac11639a: Pull complete
Digest: sha256:58666f6a49048d737eb24478e8dabce32774730e2f2d0803911a2c1f61c1b805
Status: Downloaded newer image for python:3
 ---> 038a832804a0
Step 2/7 : WORKDIR /usr/src/app
 ---> Running in baed9580915a
Removing intermediate container baed9580915a
 ---> e1dda44d0516
Step 3/7 : COPY requirements.txt ./
 ---> 378440b0c12f
Step 4/7 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 665a20dc436e
Step 6/7 : COPY . .
 ---> bff7b9c68fd1
Step 7/7 : CMD [ "python", "./app.py" ]
 ---> Running in a4cdc2564677
Removing intermediate container a4cdc2564677
 ---> ef5bc3de4d4f
Successfully built ef5bc3de4d4f
Successfully tagged cloud-native-demo:1
SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. All files and directories added to build context will have '-rwxr-xr-x' permissions. It is recommended to 
double check and reset permissions for sensitive files and directories.
```
Now if you run a **docker images** command, you should see your newly created image:
```
D:\workspaces\DockerKubesDojo>docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
cloud-native-demo                    1                   ef5bc3de4d4f        17 minutes ago      943MB
nginx                                latest              f7bb5701a33c        5 days ago          126MB
python                               3                   038a832804a0        5 days ago          932MB

```


## Run the cloud-native-demo image and expose its port

Now we are ready to run our newly created image.  To do that we are going back to the Docker run command you should be familar with.

> HINT: The string `cloud-native-demo:1` captures the coordinates of the Docker/OCI image.  It follows the pattern `{hostname to retrieve image}/{repository name}/{image name}:{tag}`.  Since we have it locally we don't specify a hostname to retrieve the image.

> HINT: The `--rm` just cleans up any remaining bits after this application runs.  It's completely stateless, so we don't need to remember anything about its execution in this scenario.

> HINT: The `-p` switch exposes the port the container listens on to your localhost interface.

```bash
docker run --rm -it -p 5000:5000 CHANGEME/cloud-native-demo:1
```

## Validate the application container is running

In your browser, navigate to the URL [http://localhost:5000](http://localhost:5000).  You should see a JSON response with some information about the running application.  If not, double check the `docker run ...` command you issued and look for any errors in the console output.

## Stop the container

In the original CLI window where you issued the `docker run ...` command, type `CTRL+C` to stop the container.
