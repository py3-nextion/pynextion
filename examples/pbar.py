import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexProgressBar
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_progressbar(port):
    nexSerial = PySerialNex(port)
    nexSerial.init()

    nexPage = NexPage(nexSerial, "pg_pbar", pid=6)

    nexProgressBar = NexProgressBar(nexSerial, "j0", cid=1)

    nexPage.show()

    time.sleep(1)

    nexProgressBar.backcolor = Colour.GRAY
    nexProgressBar.forecolor = Colour.GREEN
    nexProgressBar.value = 30

    with pytest.raises(Exception):
        nexProgressBar.value = 105  # should raise error because value must be in 0-100

    with pytest.raises(Exception):
        nexProgressBar.value = -1  # should raise error because value must be in 0-100

    time.sleep(1)

    nexSerial.close()
