from pynextion.factory import WidgetFactory
from pynextion.hardware import NexSerialMock
from pynextion.widgets import NexText


def test_widget_factory():
    nexSerial = NexSerialMock()
    widget = WidgetFactory.create(nexSerial, "Text", "t0", pid=1, cid=2)
    assert isinstance(widget, NexText)
