import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexNumber
from pynextion.constants import Colour
from pynextion.int_tools import limits


def sign_color(value, color1=Colour.GREEN, color2=Colour.RED):
    if value >= 0:
        return color1
    else:
        return color2


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_number(port):
    nexSerial = PySerialNex(port)
    nexSerial.init()

    nexPage = NexPage(nexSerial, "pg_num", pid=7)

    nexNumber = NexNumber(nexSerial, "n0", cid=1)

    nexPage.show()

    time.sleep(1)
    nexNumber.value = 1
    time.sleep(1)
    n = 2
    nexNumber.value = n
    nexNumber.backcolor = Colour.RED
    nexNumber.forecolor = Colour.WHITE

    time.sleep(1)
    assert nexNumber.value == n
    time.sleep(1)
    nexNumber.value = 3
    nexNumber.backcolor = Colour.WHITE
    nexNumber.forecolor = sign_color(n)
    time.sleep(1)

    n = -2
    nexNumber.value = n
    nexNumber.forecolor = sign_color(n)
    time.sleep(1)
    assert nexNumber.value == n

    min_val, max_val = limits(True, 32)

    n = max_val
    nexNumber.value = n
    nexNumber.forecolor = sign_color(n)
    time.sleep(1)
    assert nexNumber.value == n

    n = min_val + 1  # display only "-" is n = min_val
    nexNumber.value = n
    nexNumber.forecolor = sign_color(n)
    time.sleep(1)
    assert nexNumber.value == n

    nexSerial.close()
