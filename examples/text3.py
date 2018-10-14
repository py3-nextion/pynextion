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

    pages = [
        {
            'pid': 2, 'name': 'pg_text',
            'components': [
                {'type': 'Text', 'cid': 0, 'name': 't0'}
            ]
        }
    ]

    nexSerial.components.read_list(pages)
    nexPage = nexSerial.components.page(name="pg_text")

    nexPage.show()
    time.sleep(1)

    nexText = nexPage.widget(name="t1")
    msg = "H. by data"  # Hook
    nexText.text = msg

    nexSerial.close()
