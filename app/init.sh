#!/bin/bash

gunzip amara.db.gz
gunzip babylon.db.gz

exec "$@"
