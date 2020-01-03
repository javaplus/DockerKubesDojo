## Pass the REDIS_HOST env var as a CLI argument to the application

While our application has the ability to read directly from the configured Environment Variables, some applications are configured via CLI arguments on startup.  So far, we haven't actually told Docker or Kubernetes which Python script to run at startup.  It's been using the default `CMD` instruction defined in the original `Dockerfile` it was built from.  You can see in the `Dockerfile` in this repository, it's running the command `python app.py` by default.

This program actually accepts a few configuration values on the CLI.  Our always helpful development team left a `--help` argument in there to help discover what some of them are.  Let's run that now in a new container using Docker.  It only needs to run long enough to give us the output.  In a new console window, run the following:

```bash
docker run --rm cloud-native-demo:1 python app.py --help
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
