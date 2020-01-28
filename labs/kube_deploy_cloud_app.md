# ~~ Running in your local Kubernetes cluster ~~

Now that you know how to run a single instance, it's time to try the same in Kubernetes.  Kubernetes can orchestrate and schedule your container workloads in very flexible ways, but at the end of the day it's going to invoke a Docker or other [CRI compatible runtime](https://www.opencontainers.org/) to run your application in a similar manner as we just did.  Accomplishing this task will get us on our way towards completing our goals (what are our goals).

## Run the cloud-native-demo image in Kubernetes

Next we want to run our application in Kubernetes. 

In a console window run the following to run the `cloud-native-demo` image as a container in Kubernetes:

```bash
kubectl run cn-demo --image=cloud-native-demo:1
```

Now you can use a **kubectl get** command to see what was created. In this case, we want to see the running container which in Kubernetes is always wrapped in a Pod.  So, issue the following command to see all the current pods.

```
kubectl get pods
```

You should see a Pod that starts with the name `cn-demo-` show up.  Behind the scenes, Kubernetes is retrieving the image and executing it using Docker (in the case of the Kubernetes instance provided by Docker Desktop).  If all goes well, you should eventually see that the Pod is up and running with output in the dashboard similar to the following:

```bash
NAME                           READY   STATUS    RESTARTS   AGE
pod/cn-demo-759dc65498-j2mm6   1/1     Running   0          22s
```

## Play with the new Deployment

It's time to explore some behavior and terminology of Kubernetes.  First up is the [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod/).  We wont' go too deep on all the specifics, but a Pod is where the configuration for your running container resides.  It turns out you can run multiple containers in a single Pod, but that is outside the scope of this exercise.  To learn more about how and why you would want to do this, search around for Sidecar and Ambassador patterns.

Let's see what happens when we delete a Pod (which is one way to brute force simulate a failed container).  Run the following command, filling in the `cn-demo-***` with the unique name Kubernetes assigned your Pod, and then keep running the **kubectl get pods** command to see what happens to your pod.  Things will happen fast!

```bash
kubectl delete pod cn-demo-***
```


You deleted **that** specific Pod, but then another one with a new name showed up in its place.  That Pod is running the exact same image, and something extra in the Kubernetes cluster is making sure at least 1 of your Pods is running.  That **extra something** is called a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), and it is always working to ensure the number of Pods running for a given `Deployment` match its configured `replica` count.  The `kubectl run ...` command you just ran created a `Deployment` for you even though you didn't ask for one.  

In fact, you can see it by running **kubectl get deploy**.  

This should show the `cn-demo` deployment happily reporting that `1/1` or "1 of 1" Pods are currently available.
```
D:\workspaces\DockerKubesDojo>kubectl get deploy
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
cn-demo   1/1     1            1           9m10s

```

If you're thinking "a Deployment must be involved in how Horizontal Scaling works", you'd be right.  Let's attempt that next.

```bash
kubectl scale deployment cn-demo --replicas 3
```

Run your **kubectl get pods** again.  Do you see 3 Pods for `cn-demo-***` running?  Your `Deployment` should report `3/3` after some time as well if you run the **kubectl get deploy**

Try some other scenarios to see how Kubernetes behaves:
* Delete one of the newly created `Pods` with `kubectl delete ...`
* Scale the `Deployment` in and out, using different numbers for `--replicas`
* Do you notice anything interesting with which Pods Kubernetes decides to keep when you scale in?  Look at the time the Pod has been running.
* If you need to delete the **deployment** altogether (which will remove the pods as well) you can use this command:
```
kubectl delete deploy cn-demo

```
NOTE: If you delete it, you will have to restart it for the next labs.
Remember the command to start it is:
```bash
kubectl run cn-demo --image=cloud-native-demo:1
```

### Stretch Goal

Get up and stretch!!!  Just kidding... ok maybe that's not a bad idea... but to play more with kubernetes, let's see if we can learn how to connect to one of the running containers and get a shell so we can poke around and see the files that are in our running container.  What we will do is use the **kube exec** command to get a bash shell into one of our pods.

So, make sure you have at least one pod running, and then use the kube exec command to get a shell into the container.
The format of the kube exec command is like this:
```bash
kubectl exec -it <pod name> /bin/bash
```

NOTE: Look at the [offical documentation here](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#exec) to see what the **'-it'** is doing.  

Once you get a bash prompt issue a **pwd** command to see what the current working directory is.
Do you know why this is the working directory?

Look at the Dockerfile again that you used to create this image.

Also, do an **ls** to see all the files that were copied into this working directory and then figure out how they got there.

Now, try to actually create a new file in that directory.  You can just do a simple echo command like this:
```bash
echo "hello" > hello.txt
```
After creating the file, exit out of the shell session by simply typing **exit**.

Now, reconnect to the pod again and make sure your file is still there. (It should be).

Now, let's delete the pod and let the deployment spin up a new pod.

When your new pod finishes starting, exec into it and see if your file is still there.
Can you figure out why or why not?

<details>
  <summary>Click to expand for Answers</summary>
 
 #### Explanation
  
 - Why is the working directory "/usr/src/app"?
  - Because the [Dockerfile on line 3](https://github.com/javaplus/DockerKubesDojo/blob/42f4756afe04e07389f476a160199d7a2c12cc73/Dockerfile#L3) set the "WORKDIR" to "/usr/src/app" 
  - What does the **'-it'** do with the exec command?
    - The 'i' says pass the STDIN of your command prompt to the container
    - The 't' says the STDIN is a TTY
    - Most think of the **'-it'** just as an interactive terminal because that's what it produces.
    
  - Why did the hello.txt file disappear after deleting the pod and letting the deployment create a new one?
    - Because the container in the Pod is an instance of the image you specify.  When we added the file, we added it to that specific running instance... think of it like modifying temporary memory or modifying an instance of a class.  Once we delete that Pod that deletes that instance of the container.  Then the deployment starts up a new Pod which creates a new instance of the container off of the image we specified.  The only thing that's going to be in the running container is what we specified in the image definition (assuming we don't give special commands to the start up). 
  
  
</details>


