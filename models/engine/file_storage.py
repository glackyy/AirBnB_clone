#!/usr/bin/python3
"""This module defines a class to manage file storage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage in JSON format"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Retrieves a Dictionary of Stored Models"""
        return FileStorage.__objects

    def new(self, obj):
        """Inserts new object into storage dictionary"""
        objname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(objname, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        object_dict = {}
        for key, obj in FileStorage.__objects.items():
            object_dict[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(object_dict, file)


    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(FileStorage.__file_path, 'r') as file:
                object_dict = json.load(file)
                for key, val in object_dict.items():
                    class_name, obj_id = key.split('.')
                    _class = eval(class_name)
                    obj = _class(**val)
                    self.new(obj)
        except FileNotFoundError:
            return
