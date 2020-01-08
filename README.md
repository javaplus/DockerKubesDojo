# Docker and Kubernetes Dojo
Tutorial on Using Docker and Kubernetes

**Big thanks to [Michael Frayer](https://github.com/frayer) for most of the content of this tutorial is from him!**

## Presentation

The presentation that accompanies this workshop is available here: [docker-and-kubernetes-dojo.pdf](https://github.com/javaplus/DockerKubesDojo/blob/master/slides/docker-and-kubernetes-dojo.pdf)

This is provided to those that attended an in-person workshop who wish to reference back to topics discussed.  Much of the context is missing for those that did't attend, however it is not required material in order to proceed with the rest of the workshop below.

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

##### Linux
- [MicroK8s](https://microk8s.io/)


### Testing your Installation

Run the **docker version** command and you should see something like this:
```
C:\Users\tarltob1>docker version
Client: Docker Engine - Community
 Version:           19.03.5
 API version:       1.40
 Go version:        go1.12.12
 Git commit:        633a0ea
 Built:             Wed Nov 13 07:22:37 2019
 OS/Arch:           windows/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.5
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.12
  Git commit:       633a0ea
  Built:            Wed Nov 13 07:29:19 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
 Kubernetes:
  Version:          v1.14.8
  StackAPI:         v1beta2
```

Test kubernetes by running the **kubectl get nodes** command.
This should show you one worker node running on your machine:
```
C:\Users\tarltob1>kubectl get nodes
NAME             STATUS   ROLES    AGE   VERSION
docker-desktop   Ready    master   45d   v1.14.8

```
If these both work, you should be ready to go.


#### Optional Pre-reqs (all OS's)
##### Install Visual Studio Code

You will be editing YAML files and viewing Python code during the course of this exercise.  You can use any text editor, but Visual Studio Code is recommended.

[Download and install VS Code](https://code.visualstudio.com/)


##### Install the JSON Formatter Chrome Extension

This is a useful, but not required, Chrome extension for viewing JSON output in your browser.

[Install using a Chrome browser](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa)

---

# ~~ Labs ~~

1. [Intro to Docker and Containers](labs/docker_intro.md)

1. [Docker with Cloud Native App](labs/docker_cloud_app.md)

1. [Kubernetes Intro](labs/kube_deploy_cloud_app.md)

1. [Kubernetes Infrastructure as Code](labs/kube_infra_as_code.md)

1. [Docker for Tooling](labs/docker_tools_container.md)

1. [Kubernetes Environment Variables](labs/kube_env_vars.md)

1. [Kubernetes Override Starting Command](labs/kube_override_cmd.md)

1. [Kubernetes Ingress](labs/kube_setup_ingress.md)

1. [Kubernetes Readiness](labs/kube_readiness.md)

1. [Kubernetes Readiness Part 2](labs/kube_readiness_2.md)


---




# ~~ Conclusion ~~

This exercise has introduced you to some of the most commonly used features of Kubernetes for configuring and hosting applications using declarative, Infrastructure as Code techniques.  Even what we've shown here only begins to scratch the surface.  Here are other topics you'll want to dig deeper on as you continue your Kubernetes journey.

* [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/)
* [Declaring and using ConfigMaps to configure a Deployment](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
* [Declaring and using Secrets to configure a Deployment](https://kubernetes.io/docs/concepts/configuration/secret/)
