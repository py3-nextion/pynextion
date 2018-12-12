from .config import PORT_DEFAULT
import time
import pytest
from pynextion import PySerialNex


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_raw(port):
    nexserial = PySerialNex(port)
    
    #nexSerial.init()
    #nexserial.write("bkcmd=3")

    # nexserial.write("page 0")
    nexserial.write("page page1")
    print(nexserial.read_all())

    nexserial.write("sendme")
    time.sleep(0.1)
    print(nexserial.read_all())

    nexserial.close()
