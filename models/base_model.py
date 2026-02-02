#!/usr/bin/python3
"""Base model for HBNB models using SQLAlchemy"""

import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """Defines common attributes/methods for all models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        from models import storage
        if kwargs:
            for key, val in kwargs.items():
                if key in ["created_at", "updated_at"] and isinstance(val, str):
                    setattr(self, key, datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != "__class__":
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        """Updates updated_at and saves instance to storage"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes instance from storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Returns dictionary representation of instance"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = type(self).__name__
        if "created_at" in dictionary:
            dictionary["created_at"] = dictionary["created_at"].isoformat()
        if "updated_at" in dictionary:
            dictionary["updated_at"] = dictionary["updated_at"].isoformat()
        dictionary.pop("_sa_instance_state", None)  # Remove SQLAlchemy state
        return dictionary

    def __str__(self):
        """String representation"""
        cls_name = type(self).__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
