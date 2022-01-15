from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .ResourceRequest import ResourceRequest
from .Resource import Resource
from .Worker import Worker
