import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexButton
import datetime


def callback(sender, event):
    print("CALLBACK %s %s" % (sender, event))


@pytest.mark.parametrize("port", [PORT_DEFAULT])
@pytest.mark.parametrize("delay", [20])
def test_button(port, delay):
    nexSerial = PySerialNex(port)
    nexSerial.init()

    nexPage = NexPage(nexSerial, "pg_but", pid=8)
    nexButtonEnter = NexButton(nexSerial, "b2", cid=4)

    nexButtonEnter.callback = callback
    # button.when_pressed = callback_when_pressed
    # button.when_released = callback_when_released

    nexPage.show()

    dt_start = datetime.datetime.utcnow()
    while True:
        nexSerial.poll()
        if datetime.datetime.utcnow() - dt_start > datetime.timedelta(seconds=delay):
            break
        time.sleep(0.2)

    nexSerial.close()
