#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Class Amenity for HBNB project"""

    if STORAGE_TYPE == "db":
        __tablename__ = 'amenities'

        name = Column(String(128), nullable=False)
        # relationship for DBStorage
        place_amenities = relationship(
            "Place",
            secondary="place_amenity",
            back_populates="amenities",
            viewonly=False
        )
    else:
        # FileStorage attributes
        name = ""
