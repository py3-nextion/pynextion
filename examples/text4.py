import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
import json


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_text(port):
    nexSerial = PySerialNex(port)
    nexSerial.init()

    data = """[
    {
        "pid": 2,
        "name": "pg_text",
        "components": [
            {
                "type": "Text",
                "cid": 2,
                "name": "t0"
            },
            {
                "type": "Text",
                "cid": 3,
                "name": "t1"
            },
            {
                "type": "Text",
                "cid": 1,
                "name": "t2"
            }
        ]
    }
]"""

    pages = json.loads(data)

    nexSerial.components.read_list(pages)
    nexPage = nexSerial.components.page(name="pg_text")

    nexPage.show()
    time.sleep(1)

    nexText = nexPage.widget(name="t1")
    msg = "H. by JSON data"  # Hook
    nexText.text = msg

    nexSerial.close()
