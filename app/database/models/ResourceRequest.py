#from app.core.schemas.request import RequestSchema
from pipeline.schemas.request import RequestGet
from sqlalchemy import Column, ForeignKey, String, Integer, JSON, DateTime

from app.database.models import Base

import random
import string


def generate_id():
    id = "resource_request_" + "".join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits)
        for _ in range(15)
    )
    return id


class ResourceRequest(Base):
    __tablename__ = "resource_request"

    id = Column(String, default=generate_id, primary_key=True)

    token = Column(String)
    status = Column(Integer)
    request_json = Column(JSON)
    result_json = Column(JSON)
    result_file_url = Column(String)
    resource_url = Column(String)
    request_method = Column(String)
    time_requested = Column(DateTime)
    request_duration = Column(Integer)
    ip_address = Column(String)

    def __repr__(self):
        return "<ResourceRequest(id=%s, status=%u, url=%s, token=%s)" % (
            self.id,
            self.status,
            self.resource_url,
            self.token,
        )

    def as_schema(self):
        return RequestGet.from_orm(self)

    def as_dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "status": self.status,
            "request_json": self.request_json,
            "result_json": self.result_json,
            "resource_url": self.resource_url,
            "request_method": self.request_method,
            "time_requested": self.time_requested.timestamp(),
            "request_duration": self.request_duration,
            "ip_address": self.ip_address,
        }
