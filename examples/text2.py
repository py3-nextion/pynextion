import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexText


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_text(port):
    nexSerial = PySerialNex(port)

    print("Init")
    nexSerial.init()

    nexPage = nexSerial.components.hook_page("pg_text", pid=2)
    assert len(list(nexSerial.components.pages)) == 1
    nexText = nexPage.hook_widget(NexText, "t1", cid=1)
    assert len(list(nexPage.widgets)) == 1

    nexPage.show()
    time.sleep(1)

    msg = "H. by code"  # Hook
    nexText.text = msg

    nexSerial.close()
