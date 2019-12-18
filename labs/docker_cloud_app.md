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
