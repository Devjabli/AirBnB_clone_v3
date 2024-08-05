#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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

DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity, 
    "City": City, 
    "Place": Place,
    "Review": Review, 
    "State": State, 
    "User": User
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests for the documentation and style of DBStorage class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up for the documentation tests"""
        cls.dbs_functions = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test that tests/test_models/test_engine/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNotNone(db_storage.__doc__,
                             "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNotNone(DBStorage.__doc__,
                             "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func_name, func in self.dbs_functions:
            self.assertIsNotNone(func.__doc__,
                                 f"{func_name} method needs a docstring")
            self.assertTrue(len(func.__doc__) >= 1,
                            f"{func_name} method needs a docstring")


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(models.storage.all(), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_data = {"name": "Nairobi"}
        new_state = State(**state_data)
        models.storage.new(new_state)
        models.storage.save()

        session = models.storage._DBStorage__session
        all_objects = session.query(State).all()
        self.assertGreater(len(all_objects), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        state_data = {"name": "Kericho"}
        new_state = State(**state_data)
        models.storage.new(new_state)
        session = models.storage._DBStorage__session
        retrieved_state = session.query(State).filter_by(id=new_state.id).first()
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save, saves objects to the database"""
        state_data = {"name": "Kiambu"}
        new_state = State(**state_data)
        models.storage.new(new_state)
        models.storage.save()
        session = models.storage._DBStorage__session
        retrieved_state = session.query(State).filter_by(id=new_state.id).first()
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test to obtain instance of database storage"""
        storage = models.storage
        storage.reload()
        state_data = {"name": "Kent"}
        state_instance = State(**state_data)
        storage.new(state_instance)
        storage.save()
        retrieved_state = storage.get(State, state_instance.id)
        self.assertEqual(state_instance, retrieved_state)
        false_state_id = storage.get(State, "fake_id")
        self.assertIsNone(false_state_id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test the count method in database storage"""
        storage = models.storage
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
