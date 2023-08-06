from ramjam.utils import get_commands
from tests.stubs import stub_commands


def test_get_commands():
    assert get_commands(stub_commands) == [stub_commands.StubCommand]
