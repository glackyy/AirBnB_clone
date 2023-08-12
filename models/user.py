#!/usr/bin/python3
"""Defining User Class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Representing a User

    Attribs:
        email (str): Email of the user
        password (str): Password of the user
        first_name (str): First name of the user
        last_name (str): Last name of the user
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
