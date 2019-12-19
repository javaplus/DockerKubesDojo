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

# ~~ Intro to Docker and Containers ~~

Lab1 [Intro to Docker and Containers](labs/docker_intro.md)


# ~~ Docker with Cloud Native App ~~

Lab2 [Cloud Native App](labs/docker_cloud_app.md)


# ~~ Kubernetes Intro ~~

Lab3 [kube deploy cloud native app](labs/kube_deploy_cloud_app.md)

# ~~ Kubernetes Infrastructure as Code ~~

Lab4 [Declarative Definitions](labs/kube_infra_as_code.md)


# ~~ Docker for Kubernetes Tooling   ~~

Lab5 [Docker for Tooling](labs/docker_tools_container.md)


# ~~ Kubernetes Enviornment variables   ~~

Lab6 [Environment Variables](labs/kube_env_vars.md)


# ~~ Kubernetes Override Starting Command   ~~

Lab7 [Setting the Command to Run](labs/kube_override_cmd.md)

# ~~ Kubernetes Ingress   ~~

Lab8 [Kubernetes Ingress](labs/kube_setup_ingress.md)

# ~~ Kubernetes Detecting an Unhealthy App   ~~

Lab9 [Readiness in Kubes](labs/kube_readiness.md)

Lab10 [Readiness in Kubes Part 2](labs/kube_readiness_2.md)


---

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

# ~~ Running in your local Kubernetes cluster ~~

Now that you know how to run a single instance, it's time to try the same in Kubernetes.  Kubernetes can orchestrate and schedule your container workloads in very flexible ways, but at the end of the day it's going to invoke a Docker or other [CRI compatible runtime](https://www.opencontainers.org/) to run your application in a similar manner as we just did.  Accomplishing this task will get us on our way towards completing our goals (what are our goals).


---


---




---

---


# ~~ Conclusion ~~

This exercise has introduced you to some of the most commonly used features of Kubernetes for configuring and hosting applications using declarative, Infrastructure as Code techniques.  Even what we've shown here only begins to scratch the surface.  Here are other topics you'll want to dig deeper on as you continue your Kubernetes journey.

* [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/)
* [Declaring and using ConfigMaps to configure a Deployment](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
* [Declaring and using Secrets to configure a Deployment](https://kubernetes.io/docs/concepts/configuration/secret/)
