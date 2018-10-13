import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexNumber
from pynextion.constants import Colour
from pynextion.int_tools import limits


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_number(port):
    nexSerial = PySerialNex(port)

    nexNumber = NexNumber(nexSerial, "n0", cid=1)

    nexSerial.send("page pg_num")

    time.sleep(1)
    nexNumber.value = 1
    time.sleep(1)
    nexNumber.value = 2
    nexNumber.backcolor = Colour.RED
    nexNumber.forecolor = Colour.WHITE

    time.sleep(1)
    assert nexNumber.value == 2
    time.sleep(1)
    nexNumber.value = 3
    nexNumber.backcolor = Colour.WHITE
    nexNumber.forecolor = Colour.RED
    time.sleep(1)

    n = -2
    nexNumber.value = n
    time.sleep(1)
    assert nexNumber.value == n  # ToFix

    min_val, max_val = limits(True, 32)

    n = max_val
    nexNumber.value = n
    time.sleep(1)
    assert nexNumber.value == n

    n = min_val
    nexNumber.value = n
    time.sleep(1)
    assert nexNumber.value == n  # ToFix

    nexSerial.close()
