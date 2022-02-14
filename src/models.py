from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID as _UUID

from .app import app

db = SQLAlchemy(app)


class UUID(TypeDecorator):
    impl = _UUID(as_uuid=True)


class DataFile(db.Model):
    __tablename__ = "data_files"

    id = Column(UUID, primary_key=True, default=uuid4)
    json_body = Column(JSON, nullable=False)
    secret_token = Column(Text, nullable=False)
