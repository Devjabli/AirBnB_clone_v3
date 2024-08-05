#!/usr/bin/python3
"""
Defining FileStorage model to manipulate data to json
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """
    Representing a storage engine

    Attributes private:
        __file_path (str): where objects saved to this file.
        __objects (dict): dictionary of objects.
    """


    __file_path = "file.json"
    __objects = {}
    class_map = {
        "BaseModel": BaseModel,
        "User": User,
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State
    }

    def all(self, cls=None):
        """Returns the list of objects of one type of class.
        Args:
            cls: Class
        Return:
            returns the list of objects of one type of class.
        """
        """
        _dic = {}
        if cls is None:
            return (self.__objects)
        else:
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    _dic[key] = value
            return _dic
        """
    
        """Returns the list of objects of a specific class type.
        Args:
            cls: The class type to filter by (optional).
        
        Returns:
            A dictionary of objects of the specified class type,
            or all objects if no class type is specified.
        """
    
        if cls is None:
            return self.__objects
        return {key: value for key, value in self.__objects.items() if isinstance(value, cls)}
        
    
    def delete(self, obj=None):
        """delete obj from __objects if it’s inside
        Args:
            obj: Object
        """
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
            self.save()
        """
        """Delete obj from __objects if it exists.
    
        Args:
            obj: The object to delete.
        """
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects.pop(key, None)
            self.save()

    def new(self, obj):
        """ Sets in __objects obj with key id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """ Serializing data __objects to JSON __file_path """
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump({key: value.to_dict() for key, value in self.__objects.items()}, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception as ex:
            pass
    
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