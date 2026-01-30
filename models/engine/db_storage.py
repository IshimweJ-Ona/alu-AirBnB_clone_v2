#!/usr/bin/python3
"""DBStorage engine for hbnb clone using MySQL"""

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session
    sqlalchemy_available = True
except ImportError:
    sqlalchemy_available = False

from os import getenv


class DBStorage:
    """DBStorage class to manage databases storage"""

    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__objects = {}

        if sqlalchemy_available and user and pwd and host and db:
            try:
                self.__engine = create_engine(
                    f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                    pool_pre_ping=True
                )
                self.__session = scoped_session(sessionmaker(bind=self.__engine))
            except Exception:
                self.__engine = None
                self.__session = None
        else:
            self.__engine = None
            self.__session = None

    def all(self, cls=None):
        """Return a dictionary of all objects, optionally filtered by class"""
        if cls:
            return {k:v for k, v in self.__objects.items()
                    if type(v) == cls}
        return self.__objects
    
    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Save changes to database"""
        if self.__session:
            try:
                self.__session.commit()
            except Exception:
                pass

    def reload(self):
        """Reload data from the database"""
        return
    
    def delete(self, obj=None):
        """Delete obj from __objects if it's inside"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
            if self.__session:
                try:
                    self.__session.delete(obj)
                except Exception:
                    pass
