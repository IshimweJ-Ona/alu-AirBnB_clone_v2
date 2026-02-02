#!/usr/bin/python3
"""Base model for HBNB models using SQLAlchemy"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

# Declarative base for SQLAlchemy
Base = declarative_base()


class BaseModel:
    """Base class for all HBNB models with DBStorage support"""

    # SQLAlchemy columns
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new instance"""
        if kwargs:
            kwargs.pop("__class__", None)
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at") and isinstance(value, str):
                    # Convert ISO string to datetime
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

            # Defaults if missing
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            # New instance defaults
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

        # Add instance to storage (lazy import to avoid circular import)
        from models import storage
        storage.new(self)

    def save(self):
        """Update updated_at and save the instance to storage"""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.save()

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = type(self).__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        # Remove SQLAlchemy internal state
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def __str__(self):
        """String representation of the instance"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)
