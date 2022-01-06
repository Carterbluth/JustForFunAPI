from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import const as CONSTANTS
from contextlib import contextmanager
import logging

log = logging.getLogger()

# configure Session class with desired options
Session = sessionmaker()


def init_session():
    log.info("Preparing to init database session")
    engine = create_engine(CONSTANTS.DB_CONNECTION_STRING)
    Session.configure(bind=engine)
    print("Db started")


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
