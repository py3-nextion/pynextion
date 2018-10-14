from .objects import PID_DEFAULT, CID_DEFAULT

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


D_FACTORY = {
    "Button": NexButton,
    "Checkbox": NexCheckbox,
    "Crop": NexCrop,
    "DualStateButton": NexDualStateButton,
    "Gauge": NexGauge,
    "Hotspot": NexHotspot,
    "Number": NexNumber,
    "Page": NexPage,
    "Picture": NexPicture,
    "ProgressBar": NexProgressBar,
    "QRcode": NexQRcode,
    "Radio": NexRadio,
    "ScrollText": NexScrollText,
    "Slider": NexSlider,
    "Text": NexText,
    "Waveform": NexWaveform
}


class WidgetFactory:
    @staticmethod
    def type(typ):
        return D_FACTORY[typ]

    @staticmethod
    def create(nexserial, typ, name, pid=PID_DEFAULT, cid=CID_DEFAULT):
        return D_FACTORY[typ](nexserial, typ, pid=pid, cid=cid)
