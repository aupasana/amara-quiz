#!/bin/sh

rm docker/babylon.db
rm database/babylon.db

sqlite3 database/babylon.db < database/schema.babylon.sql

database/init_babylon.py

cp database/babylon.db docker/babylon.db
