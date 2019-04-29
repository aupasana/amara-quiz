# amara kosha

This amara kosha application has the following capabilities

- search the amarakosha (with wildcards) and show results with amara kosha context
- view amara kosha data by sarga, sloka or pada
- generate quiz questions for practice

## notes

- the underlying data is sourced from https://github.com/sanskrit-coders/uohyd/tree/master/scl-master/amarakosha
  - database/amara_mula.utf8 is forked from amara.utf8
  - database/amara_pada.csv is forked from all_kANdas
- the data has been modified to fix errors / typos
- translations have been added to the data

## Running locally via docker

- docker pull aupasana/amara-quiz
- docker run -p 8888:5000 [aupasana/amara-quiz]           // Replace [] as appropriate
- browse to http://localhost:8888

## Local development (via docker)

- Clone this repo with sub-modules (`git clone --recurse-submodules https://github.com/aupasana/amara-quiz.git`)
  - If you cloned the main repo earlier, run `git submodule update --init --recursive`
- Build a dev container (`docker build -t amara-dev -f amara-dev.dockerfile scripts`)
- Run the dev container (`docker run -p 8888:5000 -it --rm -v $(PWD):/host amara-dev bash`)
- In the dev container:
  - Go to the local sources (`cd /host`)
  - Build the databases (`./database/init_db_all.sh`)
  - Verify that the databases built correctly (`ls -la database/*.db`)
  - Run locally (`./scripts/dev_local.sh`)
- In the host, open a browser and navigate to `http://localhost:8888`
- Make changes on the host, and re-run the app from the container `cd app && python3 app.py`

## Build images

- Build the database image (`cd data_babylon && docker build -t aupasana/amara-babylon . && cd ..`)
- Build / test the app image (`scripts/docker_build_run.sh`)
