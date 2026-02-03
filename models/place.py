#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review
from models.amenity import Amenity

STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")  # detect storage type

# Many-to-many table for DBDtorage
if STORAGE_TYPE == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
        Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
    )


class Place(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Class place for HBNB"""

    if STORAGE_TYPE == "db":
        __tablename__ = 'places'

        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        # Relationship for DBStorage
        user = relationship("User", back_populates="places")
        city = relationship("City", back_populates="places")
        reviews = relationship("Review", back_populates="place", cascade="all, delete, delete-orphan")
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            back_populates="place_amenities",
            viewonly=False
        )
    else:
        # FileStorage attributes
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        from models import storage
        from models.review import Review
        from models.amenity import Amenity

        @property
        def reviews(self):
            """Return list of review instances with place_id equal current place.id"""
            return [r for r in storage.all(Review).values() if r.place_id == self.id]
        
        @property
        def amenities(self):
            """Return list of Amenity instances linked to this place"""
            all_amenities = storage.all(Amenity).values()
            return [a for a in all_amenities if a.id in self.amenity_ids]
        
        @amenities.setter
        def amenities(self, obj):
            """Add Amenity.id to amenity_ids of obj is Amenity"""
            if isinstance(obj, Amenity)and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
