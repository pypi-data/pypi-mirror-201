from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import ForeignKey
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load
from enum import Enum as ENUM

from .base import Base


class Species(ENUM):
    CARP = 'ponty'
    CATFISH = 'harcsa'
    PIKE = 'csuka'
    GRASS_CARP = 'amur'


class Catch(Base):
    __tablename__ = 'catches'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    species = Column(Enum(Species), nullable=False)
    fisher_name = Column(String(50), nullable=False)
    mass = Column(DOUBLE, nullable=False)
    length = Column(Integer, nullable=False)
    circumference = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    place_id = Column(ForeignKey('places.id'), nullable=False)
    bait = Column(String(100), nullable=False)
    gear = Column(String(200), nullable=False)
    others = Column(String(200), nullable=False)


class CatchSchema(Schema):

    model_class = Catch

    id = fields.Integer()
    species_id = fields.Integer()
    mass = fields.Float()
    length = fields.Integer()
    circumference = fields.Integer()
    time = fields.DateTime()
    place_id = fields.Integer()
    bait = fields.String()
    gear = fields.String()
    others = fields.String()

    @post_load
    def make_catch(self, data, **kwargs):
        return Catch(**data)
