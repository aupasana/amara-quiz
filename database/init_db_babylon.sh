#!/bin/sh

rm app/babylon.db
rm database/babylon.db

sqlite3 database/babylon.db < database/schema.babylon.sql

database/init_babylon.py

cp database/babylon.db data_babylon/babylon.db
cp database/babylon.db app/babylon.db