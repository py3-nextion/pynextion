
import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexGauge
from pynextion.color import NamedColor


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_gauge(port):
    nexSerial = PySerialNex(port)
    initialized = nexSerial.init()
    assert initialized

    nexPage = NexPage(nexSerial, "pg_gauge", pid=10)

    nexGauge = NexGauge(nexSerial, "z0", cid=3)

    nexPage.show()

    nexGauge.backcolor = NamedColor.WHITE
    nexGauge.forecolor = NamedColor.RED

    nexGauge.width = 3  # 0-5
    # nexGauge.pointer.width = 3  # 0-5

    # for angle in range(30, 360 + 30, 30)
    #     time.sleep(1)
    #     nexGauge.value = angle

    for angle in range(0, 360 + 6, 6):
        time.sleep(0.1)
        nexGauge.value = (angle + 90) % 360

    time.sleep(1)

    assert nexGauge.value == 90

    nexSerial.close()
