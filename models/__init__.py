#!/usr/bin/python3
"""This module instantiates the correct storage engine"""

from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    try:
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
    except ImportError:
        raise ImportError("SQLAlchemy not installed. Cannot use DBStorage")
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
