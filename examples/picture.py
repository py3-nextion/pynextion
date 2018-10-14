import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexPicture
from pynextion.resources import Picture


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_picture(port):
    nexSerial = PySerialNex(port)

    nexPage = NexPage(nexSerial, "pg_pic", pid=3)

    nexPicture = NexPicture(nexSerial, "p0", cid=1)

    nexPage.show()

    for i in range(1, 8):
        time.sleep(1)
        # nexPicture.picture = i
        nexPicture.picture = Picture(i)
        # assert nexPicture.picture == Picture(i)  # ToDo

    nexSerial.close()
