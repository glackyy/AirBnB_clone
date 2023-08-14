#!/usr/bin/python3
""" Console module for AirBnB """
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter."""

    prompt = "(hbnb) "
    classes = {"BaseModel", "State", "City",
               "Amenity", "Place", "Review", "User"}

    def do_EOF(self, line):
        """EOF Ctrl-D end of file to exit"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True
    def emptyline(self):
        """repeats line on receiving empty line"""
        pass
   
    def do_create(self, line):
        """Create instance specified by user"""
        if len(line) == 0:
            print("** class name required **")
        elif line not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            instance = eval(line)()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """Print the string representation of an instance based
           on the class name and id
        """
       if len(line) == 0:
            print("** class name required **")
            return
        args = parse(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        try:
            if args[1]:
                name = "{}.{}".format(args[0], args[1])
                if name not in storage.all().keys():
                    print("** no instance found **")
                else:
                    print(storage.all()[name])
        except IndexError:
            print("** instance id missing **")

    def do_destroy(self, line):
        """Delete an instance based on the class name and id"""
        if len(line) == 0:
            print("** class name missing **")
            return
        args = parse(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        try:
            if args[1]:
                name = "{}.{}".format(args[0], args[1])
                if name not in storage.all().keys():
                    print("** no instance found **")
                else:
                    del storage.all()[name]
                    storage.save()
        except IndexError:
            print("** instance id missing **")

    def do_all(self, arg):
        """Print all string representation of all instances
           based or not on the class name

        Args:
            arg: contains the class name to be printed
        """
        args = spliter(arg)
        objs = []
        if len(args) == 0:
            for value in storage.all().values():
                objs.append(value.__str__())
        elif args[0] not in self.__classes.keys():
            print("** class doesn't exist **")
            return False
        else:
            for val in storage.all().values():
                if args[0] == val.__class__.__name__:
                    objs.append(val.__str__())
        print(objs)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className> or <className>.all()\n")

    def do_update(self, arg):
        """Update an instance based on the class name and id
           by adding or updating attribute

        Args:
            arg (): contains the class name and id to be updated
        """
        args = spliter(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in storage.all().keys():
                print("** no instance found **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                try:
                    type(eval(args[2])) != dict
                    obj = storage.all()[key]
                    for k, v in eval(args[2]).items():
                        if k in obj.__class__.__dict__.keys():
                            val = type(obj.__class__.__dict__[k])
                            obj.__dict__[k] = val(v)
                        else:
                            obj.__dict__[k] = v
                    storage.save()
                except NameError:
                    print("** value missing **")
            else:
                obj = storage.all()[key]
                setattr(obj, args[2], args[3])
                storage.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>" +
              " or <class name>.update(<id>, <attribute name>," +
              " <attribute value>)\n")

    def default(self, line):
        """default command for handling <class name>.(actions)"""
        do_actions = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            line_ = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\(.*?\)", line_[1])
            if match is not None:
                command = [line_[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in do_actions.keys():
                    arg = "{} {}".format(line_[0], command[1])
                    do_actions[command[0]](arg)
            else:
                print("*** Unknown syntax: {}".format(line))

    def do_count(self, arg):
        """<class name>.count() Countes models"""
        args = spliter(arg)
        count = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def help_count(self):
        """ Help information for the count command """
        print("Count all objects of a class")
        print("[Usage]: count <className> or <className>.count()\n")


def spliter(arg):
    """Spliter For spliting the arg"""

    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


def parse(line):
    """Helper method to parse user typed input"""
    return tuple(line.split())


if __name__ == '__main__':
    HBNBCommand().cmdloop()
