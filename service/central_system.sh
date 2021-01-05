#!/usr/bin/env bash

export ROOTPATH=/home/ubuntu/rev_ocpp
export PYTHONPATH=$ROOTPATH/src

cd $ROOTPATH || exit
./.venv/bin/python .venv/bin/gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker