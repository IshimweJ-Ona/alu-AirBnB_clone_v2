#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__ and sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__ or not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                pline = pline[2].strip()
                if pline:
                    if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__ or not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Exit the HBNB console"""
        exit()

    def help_quit(self):
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        print("Exits the program without formatting\n")

    def emptyline(self):
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        cls_name = args_list[0]

        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        cls = HBNBCommand.classes[cls_name]
        params = args_list[1:]
        kwargs = {}

        for param in params:
            if "=" not in param:
                continue

            key, value = param.split("=", 1)

            # only set attributes that exist on the class
            if not hasattr(cls, key):
                continue

            try:
                # Quoted string value
                if value.startswith('"') and value.endswith('"'):
                    val = value[1:-1]
                    val = val.replace('\\"', '"')
                    val = val.replace("_", " ")
                else:
                    # determine expected type from class default
                    default = getattr(cls, key)
                    if isinstance(default, int):
                        val = int(value)
                    elif isinstance(default, float):
                        val = float(value)
                    elif isinstance(default, str):
                        val = value.replace("_", " ")
                    else:
                        # fallback: try int, then float, else use string
                        try:
                            val = int(value)
                        except Exception:
                            try:
                                val = float(value)
                            except Exception:
                                val = value.replace("_", " ")

                kwargs[key] = val
            except (ValueError, TypeError):
                # skip invalid parameters (e.g., non-convertible numbers)
                continue

        # create instance, then set attributes and save
        new_instance = cls()
        for k, v in kwargs.items():
            setattr(new_instance, k, v)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2].split(' ')[0] if new[2] else ''

        if not c_name:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        obj = storage.all().get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def help_show(self):
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2].split(' ')[0] if new[2] else ''

        if not c_name:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        obj = storage.all().get(key)
        if obj:
            storage.delete(obj)
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for v in storage.all().values():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k in storage.all().keys():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        args = args[2].partition(" ")
        c_id = args[0] if args[0] else ''
        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return

        # determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '\"':
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]
            args = args.partition(' ')
            if not att_name and args[0] != ' ':
                att_name = args[0]
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]
            args = [att_name, att_val]

        # update attributes
        for i, att_name in enumerate(args):
            if i % 2 == 0:
                att_val = args[i + 1]
                if not att_name:
                    print("** attribute name missing **")
                    return
                if not att_val:
                    print("** value missing **")
                    return
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)
                setattr(obj, att_name, att_val)

        obj.save()

    def help_update(self):
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
