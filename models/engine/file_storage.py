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
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        dict_ = FileStorage.__objects
        obdict = {obj: obdict[obj].todict() for obj in obdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obdict, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
           with open (FileStorage.__file_path) as f:
               object_dict = json.load(f)
               for obj in objectdict.values():
                   clsname = obj["__class__"]
                   del obj["__class__"]
                   self.new(eval(clsname)(**obj))
        except FileNotFoundError:
            return
