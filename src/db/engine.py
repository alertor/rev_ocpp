from sqlalchemy import create_engine

db_engine = create_engine('postgresql+psycopg2://user:password@localhost/rev_ocpp')
