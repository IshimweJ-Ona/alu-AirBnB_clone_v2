#!/usr/bin/python3
"""DBStorage engine for HBNB clone using MySQL and SQLAlchemy"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


classes = {
    "State": State,
    "City": City,
    "User": User,
    "Place": Place,
    "Review": Review,
    "Amenity": Amenity
}


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
        env = getenv("HBNB_ENV")

        # Only attempt DB connection if all credentials exist
        if user and pwd and host and db:
            self.__engine = create_engine(
                f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
                pool_pre_ping=True
            )
            if env == "test":
                Base.metadata.drop_all(self.__engine)
            self.reload()
        else:
            self.__engine = None
            self.__session = None

    def all(self, cls=None):
        """Query all objects of a class, or all objects"""
        if self.__session is None:
            return {}

        obj_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            for cl in classes.values():
                for obj in self.__session.query(cl).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add object to session"""
        if self.__session:
            self.__session.add(obj)

    def save(self):
        """Commit changes"""
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session"""
        if self.__session and obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and session"""
        if self.__engine:
            Base.metadata.create_all(self.__engine)
            Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
            self.__session = Session()
