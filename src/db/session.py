from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session
from .engine import db_engine

# Configure the session factory
SessionFactory = sessionmaker()
SessionFactory.configure(bind=db_engine)


@contextmanager
def session_scope(session_factory: sessionmaker):
    """Provide a transactional scope around a series of operations."""
    _session = session_factory()
    try:
        yield _session
        _session.commit()
    except (Exception, BaseException):
        _session.rollback()
        raise
    finally:
        _session.close()


async def get_db() -> Session:
    with session() as s:
        yield s


# Provide a session with context - to be invoked as `with session() as session`
def session() -> Session:
    return session_scope(SessionFactory)
