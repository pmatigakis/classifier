#!/bin/bash
set -e

if [ "$1" = "run" ]; then
    cd /app/configuration
    exec classifier-server
fi

exec "$@"
