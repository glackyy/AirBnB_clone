#!/usr/bin/python3
"""Defining City Class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Representing a city

    Attribs:
        state_id (str): id of the state
        name (str): name of the city
    """
    state_id = ""
    name = ""
