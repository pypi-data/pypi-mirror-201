from abc import ABC, abstractmethod
from typing import TypeVar
from argparse import Namespace

CommandType = TypeVar("CommandType", bound="Command")


class Command(ABC):

    args = {}
    help = ""

    def __init__(self, cli_args: Namespace) -> None:
        self.cli_args = cli_args

    @classmethod
    def method(cls) -> str:
        return cls.__name__.lower()

    @abstractmethod
    def __call__(self) -> None:
        pass
