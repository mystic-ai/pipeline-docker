from app.core.config import get_settings
import logging
import os
import json
from app.database.models import Base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker

settings = get_settings()

_database_conneciton_string = "postgresql://%s:%s@%s:%s/%s" % (
    settings.DATABASE_USERNAME,
    settings.DATABASE_PASSWORD,
    settings.DATABASE_HOSTNAME,
    settings.DATABASE_PORT,
    settings.DATABASE_NAME,
)

engine = create_engine(
    _database_conneciton_string,
    pool_size=25,
    pool_recycle=3600,
    pool_pre_ping=True,
)

if not database_exists(engine.url):
    create_database(engine.url)

database_scoped_session = scoped_session(sessionmaker(bind=engine))

Base.query = database_scoped_session.query_property()
Base.metadata.create_all(engine)

logger = logging.getLogger("uvicorn")
