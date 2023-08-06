import inspect
from types import ModuleType
from argparse import ArgumentParser, Namespace
from typing import List, Type, TypeVar, Optional
from ramjam.cli import Command

CommandModulesType = TypeVar(name="CommandModulesType", bound="CommandModules")


def get_commands(module: ModuleType, ignore: Optional[List[str]] = None) -> List[Type[Command]]:
    commands = []
    ignore = ignore or []
    for i, _class in inspect.getmembers(module, inspect.isclass):
        if _class != Command:
            if issubclass(_class, Command) and _class.method() not in ignore:
                commands.append(_class)
    return commands


def parse_args(*modules: ModuleType, ignore: Optional[List[str]] = None) -> Namespace:

    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(dest="command")
    sub_parser.required = True

    for module in modules:
        for command in get_commands(module, ignore=ignore):
            p = sub_parser.add_parser(command.method(), help=command.help)
            for args, kwargs in command.args.items():
                p.add_argument(*args, **kwargs)
            p.set_defaults(command=command)
    return parser.parse_args()
