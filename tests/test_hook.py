import pytest
from pynextion.hardware import NexSerialMock
from pynextion.widgets import NexText
from pynextion.exceptions import NexIdException, NexNameException


def test_hook():
    nexSerial = NexSerialMock()
    page = nexSerial.components.hook_page("pg_text", pid=2)
    assert len(list(nexSerial.components.pages)) == 1

    nexText1 = page.hook_widget(NexText, "t1", cid=1)  # noqa
    assert len(list(page.widgets)) == 1
    # nexText1.text = "Hello"

    with pytest.raises(NexNameException):
        page.hook_widget(NexText, "t1", cid=2)
    assert len(list(page.widgets)) == 1

    with pytest.raises(NexIdException):
        page.hook_widget(NexText, "t2", cid=1)
    assert len(list(page.widgets)) == 1

    nexText2 = page.hook_widget(NexText, "t2", cid=2)   # noqa
    assert len(list(page.widgets)) == 2
    # nexText2.text = "World"

    # new page

    page = nexSerial.components.hook_page("pg_num", pid=7)
    assert len(list(nexSerial.components.pages)) == 2

    with pytest.raises(NexNameException):
        nexSerial.components.hook_page("pg_num", pid=8)

    with pytest.raises(NexIdException):
        nexSerial.components.hook_page("pg_num2", pid=7)
