#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
from os.path import exists
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }

    def all(self):
        """Returns a dictionary of models currently in storage"""
        return self.__objects
    
    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Save storage dictionary to a file"""
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f, indent=4)

    def reload(self):
        """Loads storage dictionary from file"""
        if not exists(self.__file_path):
            return
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
            for key, val in temp.items():
                cls_name = val["__class__"]
                cls = self.classes.get(cls_name)
                if cls:
                    self.__objects[key] = cls(**val)
        except Exception:
            # Handles empty or invalid json
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
