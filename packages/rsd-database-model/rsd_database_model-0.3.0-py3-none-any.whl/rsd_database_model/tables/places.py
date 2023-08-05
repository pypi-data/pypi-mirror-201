from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load

from .base import Base


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)


class PlaceSchema(Schema):

    model_class = Place

    id = fields.Integer()
    name = fields.String()

    @post_load
    def make_place(self, data, **kwargs):
        return Place(**data)
