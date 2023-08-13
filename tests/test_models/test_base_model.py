#!/usr/bin/python3
"""Defining unittests for base_model"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        basem1 = BaseModel()
        basem2 = BaseModel()
        self.assertNotEqual(basem1.id, basem2.id)

    def test_two_models_different_created_at(self):
        basem1 = BaseModel()
        sleep(0.05)
        basem2 = BaseModel()
        self.assertLess(basem1.created_at, basem2.created_at)

    def test_two_models_different_updated_at(self):
        basem1 = BaseModel()
        sleep(0.05)
        basem2 = BaseModel()
        self.assertLess(basem1.updated_at, basem2.updated_at)

    def test_str_representation(self):
        date = datetime.today()
        date_repr = repr(dt)
        basem = BaseModel()
        basem.id = "123456"
        basem.created_at = basem.updated_at = date
        bmstr = basem.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + date_repr, bmstr)
        self.assertIn("'updated_at': " + date_repr, bmstr)

    def test_args_unused(self):
        basem = BaseModel(None)
        self.assertNotIn(None, basem.__dict__.values())

    def test_instantiation_with_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        basem = BaseModel(id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(basem.id, "345")
        self.assertEqual(basem.created_at, date)
        self.assertEqual(basem.updated_at, date)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        basem = BaseModel("12", id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(basem.id, "345")
        self.assertEqual(basem.created_at, dt)
        self.assertEqual(basem.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        basem = BaseModel()
        sleep(0.05)
        first_updated_at = basem.updated_at
        basem.save()
        self.assertLess(first_updated_at, basem.updated_at)

    def test_two_saves(self):
        basem = BaseModel()
        sleep(0.05)
        first_updated_at = basem.updated_at
        basem.save()
        second_updated_at = basem.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        basem.save()
        self.assertLess(second_updated_at, basem.updated_at)

    def test_save_with_arg(self):
        basem = BaseModel()
        with self.assertRaises(TypeError):
            basem.save(None)

    def test_save_updates_file(self):
        basem = BaseModel()
        basem.save()
        bmid = "BaseModel." + basem.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        basem = BaseModel()
        self.assertTrue(dict, type(basem.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        basem = BaseModel()
        self.assertIn("id", basem.to_dict())
        self.assertIn("created_at", basem.to_dict())
        self.assertIn("updated_at", basem.to_dict())
        self.assertIn("__class__", basem.to_dict())

    def test_to_dict_contains_added_attributes(self):
        basem = BaseModel()
        basem.name = "Holberton"
        basem.my_number = 98
        self.assertIn("name", basem.to_dict())
        self.assertIn("my_number", basem.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        basem = BaseModel()
        basem_dict = basem.to_dict()
        self.assertEqual(str, type(basem_dict["created_at"]))
        self.assertEqual(str, type(basem_dict["updated_at"]))

    def test_to_dict_output(self):
        date = datetime.today()
        basem = BaseModel()
        basem.id = "123456"
        basem.created_at = basem.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(basem.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        basem = BaseModel()
        self.assertNotEqual(basem.to_dict(), basem.__dict__)

    def test_to_dict_with_arg(self):
        basem = BaseModel()
        with self.assertRaises(TypeError):
            basem.to_dict(None)


if __name__ == "__main__":
    unittest.main()
