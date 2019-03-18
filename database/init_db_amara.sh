#!/bin/sh

rm app/amara.db
rm database/amara.db

sqlite3 database/amara.db < database/schema.amara.sql
database/create_mula_csv.pl
database/create_pada_csv.py
sqlite3 -separator ',' database/amara.db ".import database/amara_varga.csv varga"
sqlite3 -separator ',' database/amara.db ".import database/tmp_mula.csv mula"
sqlite3 -separator ',' database/amara.db ".import database/tmp_pada.csv pada"
sqlite3 -separator ',' database/amara.db ".import database/tags/final_audio.csv audio"

sqlite3 database/amara.db "update mula
set varga = ( select varga from pada where mula.varga_number = pada.varga_number )
where varga_number in ( select varga_number from pada );"

cat database/amara_pada_english.csv | cut -f 1,6 -d, > database/tmp_english.csv
cat database/amara_pada_telugu.csv | cut -f 1,6 -d, > database/tmp_telugu.csv

sqlite3 database/amara.db "delete from staging_translation;"
sqlite3 -separator ',' database/amara.db ".import database/tmp_english.csv staging_translation"
sqlite3 database/amara.db "update pada
set artha_english = ( select translation from staging_translation where pada.pada_uid = staging_translation.pada_uid )
where pada_uid in ( select pada_uid from staging_translation );"

sqlite3 database/amara.db "delete from staging_translation;"
sqlite3 -separator ',' database/amara.db ".import database/tmp_telugu.csv staging_translation"
sqlite3 database/amara.db "update pada
set artha_telugu = ( select translation from staging_translation where pada.pada_uid = staging_translation.pada_uid )
where pada_uid in ( select pada_uid from staging_translation );"

sqlite3 database/amara.db "update mula set audio_filename = ( select filename from audio where mula.sloka_line = audio.sloka_line );"
sqlite3 database/amara.db "update mula set audio_seconds = ( select seconds from audio where mula.sloka_line = audio.sloka_line );"

sqlite3 database/amara.db "delete from staging_translation;"
sqlite3 database/amara.db "vacuum;"

rm database/tmp_mula.csv
rm database/tmp_pada.csv
rm database/tmp_english.csv
rm database/tmp_telugu.csv

cp database/amara.db app/amara.db
