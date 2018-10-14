
import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexSlider
from pynextion.constants import Colour


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_slider(port):
    nexSerial = PySerialNex(port)

    nexPage = NexPage(nexSerial, "pg_slider", pid=11)

    nexSlider = NexSlider(nexSerial, "h0", cid=4)

    nexPage.show()

    time.sleep(0.1)

    nexSlider.value = 43691  # 0-65535

    time.sleep(1)

    # nexSlider.cursor.color = Colour.GRAY
    nexSlider.forecolor = Colour.GRAY

    time.sleep(1)

    w = 10
    nexSlider.cursor.width = w
    assert nexSlider.cursor.width == w

    time.sleep(1)

    h = 13
    nexSlider.cursor.height = h
    assert nexSlider.cursor.height == h

    time.sleep(1)

    nexSerial.close()
