#!/usr/bin/python3
"""Defining Amenity Class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Representing an amenity
    
    Attribs:
        name (str): name of the amenity
    """
    name = ""
