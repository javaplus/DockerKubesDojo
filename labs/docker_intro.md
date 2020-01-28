# ~~ The World of Containers ~~

### Simple Docker Run

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

Speaking of images, let's see what images you have installed locally.

Run the **Docker images** command to see the list of images on your machine.

After running this command, you should see something like this:
![Images](/labs/images/Images.png)

Notice the **hello-world** image that was downloaded when you issued the run command.

The K8s and docker images in the picture above are from the local Kubernetes installation. These K8s and Docker images were downloaded when you enabled Kubernetes on Docker Desktop.

### Run NGINX

Now we are going to run a simple [NGINX](http://nginx.org/en/) container that can be used to host web content.

We are going to use the **docker run** command again but use a different image (the nginx image) and also specify a port to expose the running container on.

Run this command:

```
docker run -p 8080:80 nginx

```
This will start a container running NGINX.  NGINX listens on port 80 by default, so we are telling Docker to expose the internal port 80 to our local port 8080.  Notice the -p for publishing ports follows the syntax of <External Port>:<Internal Port>.
 
 After running this command you should be able to open up a browser and go to http://localhost:8080 and see the nginx welcome screen.
 
 ![NGINX Welcome](/labs/images/nginxWelcome.png)
 
After hitting this in the browser, you should a log in the command prompt where you ran the container that shows a request was recieved.
By default when you run a container with the docker run command, the standard out goes to your console.  To break out and get back to your command prompt you need to hit "CTRL + C" or similar break command.

Do this now and break back to the command prompt.
NOTE: On windows, this usually does not kill the running container. On unix or mac os, this will kill the running container.

Run a [docker ps](https://docs.docker.com/engine/reference/commandline/ps/) to see the currently running containers.

You should see something like this:
```
D:\workspaces\DockerKubesDojo>docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
7e65845aa3ee        nginx               "nginx -g 'daemon of…"   4 minutes ago       Up 4 minutes        0.0.0.0:8080->80/tcp   recursing_khayyam

```
Note the **CONTAINER ID** is the unique ID for your running conatiner.  It's crucial to know if you want to do anything later with your running container... like stopping it.

If you actually, want to stop or kill the running container, you need to use the [docker stop](https://docs.docker.com/engine/reference/commandline/stop/) or the [docker kill](https://docs.docker.com/engine/reference/commandline/kill/) command.  I usually just kill them all and let the Docker gods sort em out.

However, we will be more humane and issue a docker stop command.  NOTE that you must end the command with the container id.

```
docker stop <YOUR CONTAINER ID>
```
After this, re-run your **docker ps** command and notice that the container should no longer be running.


### STRETCH GOAL 

Your mission if you choose to accept it, is to run an nginx container that hosts your own created HTML file.
You will accomplish this by using the docker run command as you did above to create an nginx container, but this time you will use a [volume mount](https://docs.docker.com/storage/volumes/) to mount a local **folder** that contains an HTML file into the running container.

To know where to mount the file so that nginx will serve it up (and see an example), read the documenation for the nginx image.  You can find it by going to http://hub.docker.com and then searching for the nginx image.  Click on the Official nginx image and scroll to the bottom to find the "How to use this image" section.  The first example is of how to host simple static content.

So, first create your own HTML file and save it to a preferably simple/short path on your hard drive (i.e. C:\dev\dojo\hello.html).

Now you will need to run the nginx container with the '-v' option and replace the "/some/content" with the path to the **folder** containing your newly created HTML.  NOTE: the example from hub.docker.com doesn't add the -p (publish port) option, so if you use it as is, you won't be able to access your nginx container... so add the "-p 8080:80" option to it along with the new volume option.  

NOTE: When you run the command the first time with a volume option, Docker will prompt you to ask you if you want to share the folder with Docker.  So, watch for a pop-up to ask you to share the folder.  Also, if you are on Windows, you are best to run this command from the basic command prompt or powershell. Using something like git bash can confuse things since it typically expect linux style paths.

Also, be aware of the docker run syntax...
```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

```




