
# development environment

1. From the `amara-quiz` directory, run `./scripts/dev_docker.sh`.
2. From inside the docker container, `cd /host` and `./scripts/dev_local.sh`
    - You may need to gunzip the databases
    - Test from `http://localhost:8888` 

# pushing changes

1. Exit docker
2. From the host system, run `./scripts/docker_build_run.sh` and test from `http://localhost:8888`
3. Push the image to docker with `./scripts/docker_push.sh`
4. Deploy to AWS using `./scripts/aws_deploy.sh`

Note: Steps 3 & 4 assume you have logged into and instantiated the docker / aws CLIs
