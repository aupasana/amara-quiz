#!/bin/sh

rm app/koshas_mulam.db
rm database/koshas_mulam.db

sqlite3 database/koshas_mulam.db < database/schema.koshas_mulam.sql

python3 database/init_koshas_mulam.py

cp database/koshas_mulam.db app/koshas_mulam.db