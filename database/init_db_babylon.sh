#!/bin/sh

# copy the output files from the sanskrit-lexicon repo into a babylon directory
# note: avoid symlinks as they don't work well docker containers
# git clone https://github.com/sanskrit-lexicon/cologne-stardict.git
# mkdir babylon
# cp /cologne-stardict/output database/babylon

rm app/babylon.db
rm database/babylon.db

sqlite3 database/babylon.db < database/schema.babylon.sql

python3 database/init_babylon.py

cp database/babylon.db data_babylon/babylon.db
gzip data_babylon/babylon.db
cp database/babylon.db app/babylon.db
