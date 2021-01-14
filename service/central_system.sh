#!/usr/bin/env bash

# TODO: Dynamically generate path when installed
export ROOTPATH=/home/ubuntu/rev_ocpp
export PYTHONPATH=$ROOTPATH/src

cd $ROOTPATH || exit
./.venv/bin/python .venv/bin/gunicorn main:app -w 8 -k uvicorn.workers.UvicornWorker