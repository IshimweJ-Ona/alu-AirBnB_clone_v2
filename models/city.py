#!/usr/bin/python3
""" City Module for HBNB project """

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    __tablename__ = "cities"

    state_id = Column(String(60), ForeignKey("states.id"), nullable=False, default="")
    name = Column(String(128), nullable=False, default="")
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    state = relationship("State", back_populates="cities")