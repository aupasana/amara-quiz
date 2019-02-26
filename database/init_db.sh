#!/bin/sh

rm docker/amara.db
sqlite3 docker/amara.db < database/schema.sql
database/create_mula_csv.pl
database/create_pada_csv.pl
sqlite3 -separator ',' docker/amara.db ".import database/tmp_mula.csv mula"
sqlite3 -separator ',' docker/amara.db ".import database/tmp_pada.csv pada"

sqlite3 docker/amara.db "update mula
set varga = ( select varga from pada where mula.varga_number = pada.varga_number )
where varga_number in ( select varga_number from pada );"

sqlite3 docker/amara.db "delete from staging_translation;"
cat database/amara_pada_english.utf8 | cut -f 1,6,7 -d, > database/tmp_english.csv
sqlite3 -separator ',' docker/amara.db ".import database/tmp_english.csv staging_translation"
sqlite3 docker/amara.db "update pada
set artha_english = ( select translation from staging_translation where pada.pada_uid = staging_translation.pada_uid )
where pada_uid in ( select pada_uid from staging_translation );"

sqlite3 docker/amara.db "delete from staging_translation;"
sqlite3 docker/amara.db "vacuum;"

rm database/tmp_mula.csv
rm database/tmp_pada.csv
rm database/tmp_english.csv
