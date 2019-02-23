# amara-quiz

This amara kosha application has the following capabilities

- search the amarakosha (with wildcards) and show results with amara kosha context
- show any sloka of the amarakosha with full details of all the words that occur (pratipadika, linga, artha)
- generates quiz words for practice and provides the meaning and relevant quotes from the amara

## notes

- code is based on docker-curriculum
- the underlying data is mastered at https://github.com/sanskrit-coders/uohyd/tree/master/scl-master/amarakosha
  - database/amara_mulam.utf8 is forked from amara.utf8
  - database/amara_pada.utf8 is forked from all_kANdas

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
