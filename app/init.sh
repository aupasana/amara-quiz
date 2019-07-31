#!/bin/sh

gunzip amara.db.gz
gunzip koshas_mulam.db.gz
gunzip babylon.db.gz

exec "$@"
