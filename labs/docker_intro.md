# ~~ The World of Containers ~~

Intro to the Docker Command Line

We are going to jump right in and make sure you can run a Docker container locally by using the [Docker run command](https://docs.docker.com/engine/reference/commandline/run/).

The typical usage of the **docker run** command is as follows:
```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```
Notice the "**IMAGE**" refers to a pre-defined docker image that will be pulled down to run.

When we say pulled down, it means the docker image must be on your machine to run, if it doesn't exist locally, then it will be downloaded/pulled before it can be run as a container.

Enough talking, let's run a container.  Issue this command:

```
docker run hello-world:latest

```
This will cause Docker to pull down the latest version of the hello-world image and then run it. 
You should see something like this:

```
C:\Users\tarltob1>docker run hello-world:latest
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:4fe721ccc2e8dc7362278a29dc660d833570ec2682f4e4194f4ee23e415e1064
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

The output from this command actually tells you what it did.  When it says that it pulled the "hello-world" image from Docker Hub, it's referring to [hub.docker.com](https://hub.docker.com/) which is the main online repository for docker images.




Maybe introduce how to create your own docker container... maybe a hello world python app so they will be more familar with the one they start to work with later. 
