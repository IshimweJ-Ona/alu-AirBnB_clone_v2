#!/usr/bin/python3
""" Unit tests for HBNB console """

import unittest
from unittest.mock import patch
from io import StringIO
import sys
from os import getenv
from console import HBNBCommand
from models.base_model import BaseModel
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
        # Should return a list (possibly empty)
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
