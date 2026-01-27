#!/usr/bin/python3
"""DBStorage engine template"""

class DBStorage:
    """"DBStorage class to manage database storage"""

    def __init__(self):
        """Initialize DBStorage"""
        self.__objects = {}

    def all(self):
        """Return a dictionary of all objects"""
        return self.__objects
    
    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        pass

    def reload(self):
        pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
