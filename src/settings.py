import os


MONGO_ADDR = 'mongodb://ocppdb:27017'
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

PG_ADDR = 'ocppdb'
PG_DB = 'rev_ocpp'
PG_USER = os.environ.get('PG_USER')
PG_PASS = os.environ.get('PG_PASS')