import os


MONGO_ADDR = os.environ['MONGO_ADDR']
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

# Dict access to throw key error if they are not present
PG_ADDR = os.environ['PG_ADDR']
PG_DB = os.environ['PG_DB']
PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']

# Auth stuff
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
