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
            if "__class__" in kwargs:
                kwargs.pop("__class__")

            if "created_at" not in kwargs or "updated_at" not in kwargs:
                raise KeyError("'created_at' and 'updated_at' are required")
            
            if "id" in kwargs and not isinstance(kwargs["id"], str):
                raise TypeError("id must be a string")
            
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    if not isinstance(value, str):
                        raise TypeError(f"{key} must be a string")
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            storage.new(self)

    def __str__(self):
        """String representation of the instance"""
        cls_name = type(self).__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
    
    def save(self):
        """Updates updated_at and saves the instance to storage"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = type(self).__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary
