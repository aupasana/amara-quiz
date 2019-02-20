#!/bin/sh

rm docker/amara.db
sqlite3 docker/amara.db < database/schema.sql
database/init_all_slokas.sh
database/init_pada_csv.pl
sqlite3 -separator ',' docker/amara.db ".import database/tmp_tokens.csv pada"
