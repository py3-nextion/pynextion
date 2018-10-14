from pynextion.widgets import (
    NexButton,
    NexCheckbox,
    NexCrop,
    NexDualStateButton,
    NexGauge,
    NexHotspot,
    NexNumber,
    NexPage,
    NexPicture,
    NexProgressBar,
    NexQRcode,
    NexRadio,
    NexScrollText,
    NexSlider,
    NexText,
    NexWaveform
)
from pynextion.hardware import NexSerialMock


def test_widgets_init():
    controls = [
        NexButton,
        NexCheckbox,
        NexCrop,
        NexDualStateButton,
        NexGauge,
        NexHotspot,
        NexNumber,
        NexPage,
        NexPicture,
        NexProgressBar,
        NexQRcode,
        NexRadio,
        NexScrollText,
        NexSlider,
        NexText,
        NexWaveform
    ]
    nexSerial = NexSerialMock()
    name, pid, cid = "t0", 0, 0
    for ctl in controls:
        ctl(nexSerial, name, pid=pid, cid=cid)
