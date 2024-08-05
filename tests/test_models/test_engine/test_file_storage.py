#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

FileStorage = file_storage.FileStorage
classes = {
    "Amenity": Amenity, 
    "BaseModel": BaseModel, 
    "City": City,
    "Place": Place, 
    "Review": Review, 
    "State": State, 
    "User": User
}


class TestFileStorageDocs(unittest.TestCase):
    """Tests for the documentation and style of FileStorage class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up for the documentation tests"""
        cls.fs_functions = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_engine/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNotNone(file_storage.__doc__,
                             "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNotNone(FileStorage.__doc__,
                             "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func_name, func in self.fs_functions:
            self.assertIsNotNone(func.__doc__,
                                 f"{func_name} method needs a docstring")
            self.assertTrue(len(func.__doc__) >= 1,
                            f"{func_name} method needs a docstring")


class TestFileStorage(unittest.TestCase):
    """Tests for the FileStorage class"""
    
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attribute"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertIsInstance(new_dict, dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """Test that new adds an object to the FileStorage.__objects attribute"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get(self):
        """Test to obtain an instance from file storage"""
        storage = FileStorage()
        storage.reload()
        state_data = {"name": "Kent"}
        state_instance = State(**state_data)
        storage.new(state_instance)
        storage.save()
        retrieved_state = storage.get(State, state_instance.id)
        self.assertEqual(state_instance, retrieved_state)
        false_state_id = storage.get(State, "fake_id")
        self.assertIsNone(false_state_id)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count(self):
        """Test the count method in file storage"""
        storage = FileStorage()
        storage.reload()
        state_data = {"name": "Gent"}
        state_instance = State(**state_data)
        storage.new(state_instance)
        city_data = {"name": "Gent", "state_id": state_instance.id}
        city_instance = City(**city_data)
        storage.new(city_instance)
        storage.save()

        state_occurrence = storage.count(State)
        self.assertEqual(state_occurrence, len(storage.all(State)))
        all_occurrence = storage.count()
        self.assertEqual(all_occurrence, len(storage.all()))
