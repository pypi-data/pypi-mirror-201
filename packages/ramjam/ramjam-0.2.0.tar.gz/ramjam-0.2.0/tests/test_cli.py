import pytest
from argparse import Namespace
from ramjam.cli import Command


def test_method():
    class MyCommand(Command):
        pass

    assert MyCommand.method() == "mycommand"


def test_call():
    class MyCommand(Command):
        pass

    with pytest.raises(TypeError):
        MyCommand(Namespace())  # Cannot instantiate abstract class


def test_args():
    class MyCommand(Command):
        args = {"--foo": {"help": "Foo help"}}

    assert MyCommand.args == {"--foo": {"help": "Foo help"}}


def test_help():
    class MyCommand(Command):
        help = "Some help"

    assert MyCommand.help == "Some help"


def test_cli():
    class MyCommand(Command):
        args = {"--foo": {"help": "Foo help"}}
        help = "Some help"

        def __call__(self) -> None:
            pass

    args = Namespace(command=MyCommand, foo="bar")
    assert MyCommand(args).cli_args == args
