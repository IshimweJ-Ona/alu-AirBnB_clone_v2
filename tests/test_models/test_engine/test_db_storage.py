#!/usr/bin/python3
"""Unit tests for DBStorage engine"""

import unittest
from os import getenv

# Check if sqlalchemy is available
try:
    from models.engine.db_storage import DBStorage
    sqlalchemy_available = True
except ImportError:
    sqlalchemy_available = False

from models.base_model import BaseModel


@unittest.skipUnless(sqlalchemy_available, "SQLAlchemy not installed")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level resources"""
        cls.storage = DBStorage()

    def setUp(self):
        """Clear objects before each test"""
        # Reinitialize storage to clear objects
        self.storage = DBStorage()

    def test_all_returns_dict(self):
        """all() should return a dictionary"""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_new_adds_object(self):
        """new() should add an object to __objects"""
        bm = BaseModel()
        self.storage.new(bm)
        key = f"BaseModel.{bm.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], bm)

    def test_delete_removes_object(self):
        """delete() should remove an object from __objects"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.delete(bm)
        self.assertNotIn(f"BaseModel.{bm.id}", self.storage.all())

    def test_all_with_cls_none(self):
        """all(cls=None) should return all objects"""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.storage.new(bm1)
        self.storage.new(bm2)
        all_objs = self.storage.all()
        self.assertEqual(len(all_objs), 2)

    def test_all_with_cls_argument(self):
        """Optional: check filtering by class if implemented"""
        # DBStorage.all(cls=...) currently does not filter
        bm = BaseModel()
        self.storage.new(bm)
        result = self.storage.all(BaseModel)
        self.assertIn(f"BaseModel.{bm.id}", result)

    def test_save_placeholder(self):
        """save() exists but does nothing yet"""
        try:
            self.storage.save()
        except Exception as e:
            self.fail(f"save() raised an exception: {e}")

    def test_reload_placeholder(self):
        """reload() exists but does nothing yet"""
        try:
            self.storage.reload()
        except Exception as e:
            self.fail(f"reload() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
