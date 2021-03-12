MONGO_ADDR = 'mongodb://127.0.0.1:27018/'
MONGO_USER = 'user'
MONGO_PASS = 'password'

# Dict access to throw key error if they are not present
PG_ADDR = 'localhost'
PG_DB = 'rev_ocpp'
PG_USER = 'user'
PG_PASS = 'password'

# Auth stuff
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
DEFAULT_JWT_EXPIRE_MINS = 30

ORIGINS = [
    'http://localhost:8000',
    'http://localhost:4200'
]