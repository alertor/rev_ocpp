from sqlalchemy import create_engine

import settings

db_engine = create_engine(
    f'postgresql+psycopg2://{settings.PG_USER}:{settings.PG_PASS}@{settings.PG_ADDR}/{settings.PG_DB}'
)
