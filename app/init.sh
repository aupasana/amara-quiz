#!/bin/sh

gunzip amara.db.gz
gunzip babylon.db.gz

exec "$@"
