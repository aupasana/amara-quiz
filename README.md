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

## Building locally

- Clone this repo
- database/init_db.sh                                     // Requires sqlite3 and perl
- docker build -t [aupasana/amara-quiz] .                 // Replace [] as appropriate
- docker run -p 8888:5000 [aupasana/amara-quiz]           // Replace [] as appropriate
- browse to http://localhost:8888
