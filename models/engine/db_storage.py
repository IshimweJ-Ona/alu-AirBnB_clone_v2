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

classes = {
    "State": State,
    "City": City,
    "User": User,
    "Place": Place
}

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        if user and pwd and host and db:
            self.__engine = create_engine(
                f"mysql+pymysql://{user}:{pwd}@{host}/{db}",
                pool_pre_ping=True
            )
            if env == "test":
                Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        obj_dict =  {}
        if self.__session:
            if cls:
                cls_type = classes.get(cls) if isinstance(cls, str) else cls
                if cls_type is not None:
                    for obj in self.__session.query(cls_type).all():
                        obj_dict[f"{type(obj).__name__}.{obj.id}"] = obj
            else:
                for cl in classes.values():
                    if cl is not None:
                        for obj in self.__session.query(cl).all():
                            obj_dict[f"{type(obj).__name__}.{obj.id}"] = obj
        return obj_dict
    
    def new(self, obj):
        if self.__session:
            self.__session.add(obj)

    def save(self):
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        if self.__session and obj:
            self.__session.delete(obj)

    def reload(self):
        if self.__engine:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(session_factory)
            self.__session = Session()
