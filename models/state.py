#!/usr/bin/python3
""" State Module for HBNB project """

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv


class State(BaseModel, Base):
    """State class for HBNB project"""
    __tablename__ = "states"

    name = Column(String(128), nullable=False, default="")


# Conditional assignment depending on storage type
if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.city import City
    State.cities = relationship("City", back_populates="state",
                                cascade="all, delete")
else:
    from models import storage
    from models.city import City

    @property
    def cities(self):
        """Return list of City instances with state_id matching this State"""
        all_cities = storage.all(City)
        return [city for city in all_cities.values()
                if city.state_id == self.id]

    State.cities = cities
