#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    """Database storage engine using SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects"""
        objects = {}
        classes = [State, City, User, Amenity, Place, Review]
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        else:
            for cls_ in classes:
                query = self.__session.query(cls_).all()
                for obj in query:
                    objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return objects

    def new(self, obj):
        """Add object to session"""
        self.__session.add(obj)

    def save(self):
        """Commit session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
