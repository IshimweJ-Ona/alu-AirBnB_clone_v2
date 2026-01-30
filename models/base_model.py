#!/usr/bin/python3
"""Base model for all HBNB models"""
import uuid
from datetime import datetime, timedelta


class BaseModel:
    """Defines common attributes/methods for all models"""

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now() + timedelta(microseconds=1)
            storage.new(self)
        else:
            for key in kwargs.keys():
                if not isinstance(key, str):
                    raise TypeError("keys must be strings")
            if 'created_at' not in kwargs or 'updated_at' not in kwargs:
                raise KeyError("'created_at' and 'updated_at' are required")
            if 'id' in kwargs and not isinstance(kwargs['id'], str):
                raise TypeError("id must be a string")

            kwargs['created_at'] = datetime.strptime(kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
            kwargs.pop('__class__', None)
            self.__dict__.update(kwargs)

    def __str__(self):
        """String representation of the instance"""
        cls_name = type(self).__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)

    def save(self):
        """Updates updated_at and saves the instance to storage"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = type(self).__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary
