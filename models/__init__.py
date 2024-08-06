#!/usr/bin/python3
""" Importing models file_storage to use -> storage"""
from os import getenv


type_storage = getenv('HBNB_TYPE_STORAGE')


if type_storage == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()