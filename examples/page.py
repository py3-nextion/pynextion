import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage


@pytest.mark.parametrize("port", [PORT_DEFAULT])
def test_page(port):
    nexserial = PySerialNex(port)
    pages = ["page0", "page1", "pg_text", "pg_pic",
             "pg_var", "pg_scroll", "pg_pbar",
             "pg_num", "pg_but", "pg_qr", "pg_gauge",
             "pg_slider", "pg_waveform", "pg_dsb_chk_rad",
             "pg_hotspot", "pg_crop", "pg_timer", "pg_num_kb",
             "keybdB", "pg_text_kb", "keybdC", "keydbA"]
    nexpages = []
    assert len(pages) == 22
    for i, name in enumerate(pages):
        page = NexPage(nexserial, name, i)
        nexpages.append(page)

    for page in nexpages:
        print(page.show())
        time.sleep(0.5)

    page = nexpages[0]
    page.show()

    time.sleep(2)

    assert nexserial.current_page == page.pid

    assert nexpages[0].ishown()
    assert not nexpages[1].ishown()

    nexserial.close()
