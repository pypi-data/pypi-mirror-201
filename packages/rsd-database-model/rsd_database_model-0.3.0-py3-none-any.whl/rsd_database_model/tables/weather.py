from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import ForeignKey
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load

from .base import Base


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    place_id = Column(ForeignKey('places.id'), nullable=False)
    time = Column(DateTime, nullable=False)
    temperature = Column(DOUBLE, nullable=False)
    temperature_min = Column(DOUBLE, nullable=False)
    temperature_max = Column(DOUBLE, nullable=False)
    feels_like = Column(DOUBLE, nullable=False)
    pressure = Column(DOUBLE, nullable=False)
    humidity = Column(DOUBLE, nullable=False)
    dew_point = Column(DOUBLE, nullable=False)
    clouds = Column(DOUBLE, nullable=False)
    rain = Column(DOUBLE, nullable=False)
    snow = Column(DOUBLE, nullable=False)
    wind_speed = Column(DOUBLE, nullable=False)
    wind_deg = Column(DOUBLE, nullable=False)
    wind_gust = Column(DOUBLE, nullable=False)


class WeatherSchema(Schema):

    model_class = Weather

    id = fields.Integer()
    place_id = fields.Integer()
    time = fields.DateTime()
    temperature = fields.Float()
    temperature_min = fields.Float()
    temperature_max = fields.Float()
    feels_like = fields.Float()
    pressure = fields.Float()
    humidity = fields.Float()
    dew_point = fields.Float()
    clouds = fields.Float()
    rain = fields.Float()
    snow = fields.Float()
    wind_speed = fields.Float()
    wind_deg = fields.Float()
    wind_gust = fields.Float()

    @post_load
    def make_weather(self, data, **kwargs):
        return Weather(**data)
