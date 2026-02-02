#!/usr/bin/python3
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models

class State(BaseModel, Base):
    """State class"""
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if models.storage.__class__.__name__ == 'DBStorage':
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        @property
        def cities(self):
            """Return list of City instances related to this State"""
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
