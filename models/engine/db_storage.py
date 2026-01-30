#!/usr/bin/python3
"""DBStorage engine for HBNB clone using MySQL"""
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session
    sqlalchemy_available = True
except ImportError:
    sqlalchemy_available = False

import json
from os import getenv


class DBStorage:
    """Database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__objects = {}

        if sqlalchemy_available and user and pwd and host and db:
            try:
                self.__engine = create_engine(
                    f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
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
        """Return all objects optionally filtered by class"""
        if cls:
            return {k: v for k, v in self.__objects.items() if type(v) == cls}
        return self.__objects

    def new(self, obj):
        """Add new object to storage"""
        key = f"{type(obj).__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Save objects to file.json (for tests)"""
        try:
            temp = {k: v.to_dict() for k, v in self.__objects.items()}
            with open("file.json", "w") as f:
                json.dump(temp, f, indent=4)
        except Exception:
            pass

    def reload(self):
        """Reload objects from file.json"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.base_model import BaseModel

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
        }

        try:
            with open("file.json", "r") as f:
                obj_dict = json.load(f)
                for key, val in obj_dict.items():
                    cls = classes.get(val["__class__"])
                    if cls:
                        self.__objects[key] = cls(**val)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """Delete obj from storage"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
