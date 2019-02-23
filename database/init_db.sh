#!/bin/sh

rm docker/amara.db
sqlite3 docker/amara.db < database/schema.sql
database/create_sloka_csv.pl
database/create_pada_csv.pl
sqlite3 -separator ',' docker/amara.db ".import database/tmp_sloka_lines.csv mula"
sqlite3 -separator ',' docker/amara.db ".import database/tmp_tokens.csv pada"
rm database/tmp_sloka_lines.csv
rm database/tmp_tokens.csv
