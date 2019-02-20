# amara-quiz

This amara kosha application has the following capabilities

- generates quiz words for practice and provides the meaning and relevant quotes from the amara
- allows basic search (with wildcards) of amara kosha words

## notes

- code is based on docker-curriculum
- the underlying data is mastered at https://github.com/sanskrit-coders/uohyd/tree/master/scl-master/amarakosha
  - amara_mulam.utf8 is forked from amara.utf8
  - amara_tokens*.utf8 is forked from all_kANdas

## Running locally via docker

- docker pull aupasana/amara-quiz
- docker run -p 8888:5000 [aupasana/amara-quiz]           // Replace [] as appropriate
- browse to http://localhost:8888

## Building locally

- Clone this repo
- database/init_db.sh                                     // Requires various dependencies including sqlite3, xmlstarlet, gsed
- docker build -t [aupasana/amara-quiz] .                 // Replace [] as appropriate
- docker run -p 8888:5000 [aupasana/amara-quiz]           // Replace [] as appropriate
- browse to http://localhost:8888
