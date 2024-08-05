#!/usr/bin/python3
"""Engine DBStorage Module"""

from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


class DBStorage:
    """New Engine for database storage
    
    Attributes:
        __engine (Engine): SQLAlchemy engine.
        __session (Session): SQLAlchemy session.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializing the storage engine."""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB))

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name.
        
        Args:
            cls (class, optional): Class to filter objects. Defaults to None.
        
        Returns:
            dict: Dictionary of objects.
        """
        clss = [State, City, User, Place, Review, Amenity]
        result = {}

        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = [obj for cls in clss for obj in self.__session.query(cls).all()]

        for obj in objs:
            key = f"{type(obj).__name__}.{obj.id}"
            result[key] = obj

        return result


    def new(self, obj):
        """Adding object current of database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commiting all changes current of database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deleting from current of database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize session."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Close the current session."""
        self.__session.close()
    
    def get(self, cls, id):
        """ Retrieving data """
        if cls in self.class_map.values() and id and type(id) == str:
            dic_obj = self.all(cls)
            for k, v in dic_obj.items():
                if k.split(".")[1] == id:
                    return v
        return None
    
    def count(self, cls=None):
        """ counters """
        data = self.all(cls)
        if cls in self.class_map.value():
            data = self.all(cls)
        return len(data)
