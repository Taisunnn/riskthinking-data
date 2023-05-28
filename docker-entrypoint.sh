#!/bin/bash
set -e

case "$1" in
    start)
        airflow standalone
        ;;
    test)
        PYTHONPATH=dags pytest dags
        ;;
    *)
        exec "$@"
        ;;
esac
