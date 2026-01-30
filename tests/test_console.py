#!/usr/bin/python3
""" Unit tests for HBNB console """

import unittest
from unittest.mock import patch
from io import StringIO
import sys
from os import getenv
from console import HBNBCommand
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.__init__ import storage


class TestConsole(unittest.TestCase):
    """Test the console commands"""

    def setUp(self):
        """Redirect stdout for testing"""
        self.console = HBNBCommand()
        self.held_stdout = StringIO()
        sys.stdout = self.held_stdout

    def tearDown(self):
        """Restore stdout"""
        sys.stdout = sys.__stdout__

    def get_output(self):
        """Get stdout output"""
        return self.held_stdout.getvalue().strip()

    def test_quit(self):
        """Test quit command exits"""
        with self.assertRaises(SystemExit):
            self.console.onecmd("quit")

    def test_EOF(self):
        """Test EOF command exits"""
        with self.assertRaises(SystemExit):
            self.console.onecmd("EOF")

    def test_create_missing_class(self):
        self.console.onecmd("create")
        output = self.get_output()
        self.assertEqual(output, "** class name missing **")

    def test_create_invalid_class(self):
        self.console.onecmd("create InvalidClass")
        output = self.get_output()
        self.assertEqual(output, "** class doesn't exist **")

    def test_create_valid_class(self):
        self.console.onecmd("create BaseModel")
        output = self.get_output()
        # check if an id is printed (UUID length 36)
        self.assertEqual(len(output), 36)

    def test_create_with_params(self):
        """Test create with string parameter"""
        self.console.onecmd('create State name="California"')
        output = self.get_output()
        self.assertEqual(len(output), 36)
        key = "State." + output
        obj = storage.all().get(key)
        self.assertEqual(obj.name, "California")

    def test_create_with_int_param(self):
        """Test create with integer parameter"""
        self.console.onecmd('create Place number_rooms=4')
        output = self.get_output()
        self.assertEqual(len(output), 36)
        key = "Place." + output
        obj = storage.all().get(key)
        self.assertEqual(obj.number_rooms, 4)

    def test_create_with_float_param(self):
        """Test create with float parameter"""
        self.console.onecmd('create Place latitude=37.773972')
        output = self.get_output()
        self.assertEqual(len(output), 36)
        key = "Place." + output
        obj = storage.all().get(key)
        self.assertEqual(obj.latitude, 37.773972)

    def test_create_with_multiple_params(self):
        """Test create with multiple parameters"""
        cmd = ('create Place city_id="0001" user_id="0001" '
               'name="My_little_house" number_rooms=4 number_bathrooms=2 '
               'max_guest=10 price_by_night=300 latitude=37.773972 '
               'longitude=-122.431297')
        self.console.onecmd(cmd)
        output = self.get_output()
        self.assertEqual(len(output), 36)
        key = "Place." + output
        obj = storage.all().get(key)
        self.assertEqual(obj.name, "My little house")
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 10)
        self.assertEqual(obj.price_by_night, 300)
        self.assertEqual(obj.latitude, 37.773972)
        self.assertEqual(obj.longitude, -122.431297)

    def test_create_skips_invalid_params(self):
        """Test invalid params are skipped or handled correctly"""
        # unquoted strings should be accepted as strings; invalid numeric params should be skipped
        self.console.onecmd('create State name=California population=abc')
        output = self.get_output()
        self.assertEqual(len(output), 36)
        key = "State." + output
        obj = storage.all().get(key)
        self.assertTrue(hasattr(obj, "name"))
        self.assertEqual(obj.name, "California")
        self.assertFalse(hasattr(obj, "population"))

    def test_show_missing_class(self):
        self.console.onecmd("show")
        output = self.get_output()
        self.assertEqual(output, "** class name missing **")

    def test_show_invalid_class(self):
        self.console.onecmd("show InvalidClass 123")
        output = self.get_output()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_missing_id(self):
        self.console.onecmd("show BaseModel")
        output = self.get_output()
        self.assertEqual(output, "** instance id missing **")

    def test_show_nonexistent_instance(self):
        self.console.onecmd("show BaseModel 1234")
        output = self.get_output()
        self.assertEqual(output, "** no instance found **")

    def test_all_command(self):
        self.console.onecmd("all")
        output = self.get_output()
        self.assertTrue(output.startswith('[') and output.endswith(']'))

    def test_count_command(self):
        self.console.onecmd("count BaseModel")
        output = self.get_output()
        self.assertTrue(output.isdigit())

    def test_destroy_missing_class(self):
        self.console.onecmd("destroy")
        output = self.get_output()
        self.assertEqual(output, "** class name missing **")

    def test_destroy_invalid_class(self):
        self.console.onecmd("destroy InvalidClass 123")
        output = self.get_output()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_missing_id(self):
        self.console.onecmd("destroy BaseModel")
        output = self.get_output()
        self.assertEqual(output, "** instance id missing **")

    def test_update_missing_class(self):
        self.console.onecmd("update")
        output = self.get_output()
        self.assertEqual(output, "** class name missing **")

    def test_update_invalid_class(self):
        self.console.onecmd("update InvalidClass 123 name test")
        output = self.get_output()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_missing_id(self):
        self.console.onecmd("update BaseModel")
        output = self.get_output()
        self.assertEqual(output, "** instance id missing **")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db",
                     "DBStorage not yet implemented")
    def test_dbstorage_skip(self):
        """Test skipped for DBStorage"""
        pass


if __name__ == '__main__':
    unittest.main()
