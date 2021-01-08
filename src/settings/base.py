import os


MONGO_ADDR = os.environ['MONGO_ADDR']
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

# Dict access to throw key error if they are not present
PG_ADDR = os.environ['PG_ADDR']
PG_DB = os.environ['PG_DB']
PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']