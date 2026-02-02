#!/usr/bin/python3
""" State Module for HBNB project """

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv


class State(BaseModel, Base):
    __tablename__ = "states"

    name = Column(String(128), nullable=False, default="")

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """Return list of City instance with state_id matching this state"""
            from models import storage
            from models.city import City
            all_cities = storage.all(City)
            return [city for city in all_cities.values()
                    if city.state_id == self.id]
