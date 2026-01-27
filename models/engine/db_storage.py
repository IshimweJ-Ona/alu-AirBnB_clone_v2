#!/usr/bin/python3
"""DBStorage engine for hbnb clone using MySQL"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """DBStorage class to manage database storage"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}/{db}',
                                      pool_pre_ping=True)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        self.__objects = {}

    def all(self, cls=None):
        """Return a dictionary of all objects of class cls"""
        return self.__objects
    
    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Save changes to database"""
        pass

    def reload(self):
        pass

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
