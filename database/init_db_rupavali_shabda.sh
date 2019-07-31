#!/bin/sh

rm app/rupavali_shabda.db
rm database/rupavali_shabda.db

sqlite3 database/rupavali_shabda.db < database/schema.rupavali_shabda.sql

python3 database/init_rupavali_shabda.py

cp database/rupavali_shabda.db app/rupavali_shabda.db