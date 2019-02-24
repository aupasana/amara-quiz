#!/bin/sh

rm docker/amara.db
sqlite3 docker/amara.db < database/schema.sql
database/create_mula_csv.pl
database/create_pada_csv.pl
sqlite3 -separator ',' docker/amara.db ".import database/tmp_mula.csv mula"
sqlite3 -separator ',' docker/amara.db ".import database/tmp_pada.csv pada"

sqlite3 docker/amara.db "update mula
set varga = ( select varga from pada where mula.sloka_line = pada.sloka_line )
where sloka_line in ( select sloka_line from pada );"

# rm database/tmp_mula.csv
# rm database/tmp_pada.csv
