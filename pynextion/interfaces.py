from .constants import (
    Alignment
)

from .resources import (
    Font,
    Picture
)
from .events import Event


class NxInterface:
    def _send(self, cmd):
        return self._nid._nexserial.send(cmd)

    def _get_nex_boolean_property(self, prop):
        name = self._nid.name
        cmd = "get %s.%s" % (name, prop)
        return self._nid._nexserial.get_nex_bool_command(cmd)

    def _set_nex_boolean_property(self, prop, value):
        name = self._nid.name
        if value:
            value = 1
        else:
            value = 0
        cmd = "%s.%s=%s" % (name, prop, value)
        return self._nid._nexserial.set_nex_bool_command(cmd)

    def _get_nex_number_property(self, prop, signed, bit_size):
        name = self._nid.name
        cmd = "get %s.%s" % (name, prop)
        return self._nid._nexserial.get_nex_number_command(cmd, signed, bit_size)

    def _set_nex_number_property(self, prop, value):
        name = self._nid.name
        cmd = "%s.%s=%s" % (name, prop, value)
        return self._nid._nexserial.set_nex_number_command(cmd)

    def _get_nex_string_property(self, prop):
        name = self._nid.name
        cmd = "get %s.%s" % (name, prop)
        return self._nid._nexserial.get_nex_string_command(cmd)

    def _set_nex_string_property(self, prop, value):
        name = self._nid.name
        cmd = "%s.%s=\"%s\"" % (name, prop, value)
        return self._nid._nexserial.set_nex_string_command(cmd)


class INumericalUnsignedValued(NxInterface):
    @property
    def value(self):
        return self._get_nex_number_property("val", False, 32)

    @value.setter
    def value(self, value):
        self._set_nex_number_property("val", value)


class INumericalSignedValued(NxInterface):
    @property
    def value(self):
        return self._get_nex_number_property("val", True, 32)

    @value.setter
    def value(self, value):
        self._set_nex_number_property("val", value)


class IBooleanValued(NxInterface):
    @property
    def value(self):
        # return bool(self.get_nex_number_property("val", False, 32))
        return self._get_nex_boolean_property("val")

    @value.setter
    def value(self, value):
        value = bool(value)
        self._set_nex_boolean_property("val", value)


class IStringValued(NxInterface):
    @property
    def text(self):
        return self._get_nex_string_property("txt")

    @text.setter
    def text(self, value):
        self._set_nex_string_property("txt", value)


class IColourable(NxInterface):
    @property
    def backcolor(self):
        return self._get_nex_number_property("bco", False, 32)

    @backcolor.setter
    def backcolor(self, color):
        self._set_nex_number_property("bco", color.value)

    @property
    def forecolor(self):
        return self._get_nex_number_property("pco", False, 32)

    @forecolor.setter
    def forecolor(self, color):
        self._set_nex_number_property("pco", color.value)


class AlignmentDirection(NxInterface):
    def __init__(self, nid):
        self._nid = nid

    @property
    def vertical(self):
        return Alignment.Vertical(self._get_nex_number_property("ycen", False, 32))

    @vertical.setter
    def vertical(self, value):
        assert isinstance(value, Alignment.Vertical), "Argument must be %r" % Alignment.Vertical
        self._set_nex_number_property("ycen", value.value)

    @property
    def horizontal(self):
        return Alignment.Horizontal(self._get_nex_number_property("xcen", False, 32))

    @horizontal.setter
    def horizontal(self, value):
        assert isinstance(value, Alignment.Horizontal), "Argument must be %r" % Alignment.Horizontal
        self._set_nex_number_property("xcen", value.value)


class IFontStyleable(NxInterface):
    @property
    def font(self):
        return self._get_nex_number_property("font", False, 32)

    @font.setter
    def font(self, value):
        assert isinstance(value, Font), "Argument must be %r" % Font
        self._set_nex_number_property("font", value.id)

    @property
    def alignment(self):
        return AlignmentDirection(self._nid)


class IPicturable(NxInterface):
    @property
    def picture(self):
        return self._get_nex_number_property("pic", False, 32)

    @picture.setter
    def picture(self, value):
        assert isinstance(value, Picture), "Argument must be %r" % Picture
        self._set_nex_number_property("pic", value.id)


class IViewable(NxInterface):
    @property
    def visible(self):
        oid = self.nid.name
        return self._send("vis %s" % oid)

    @visible.setter
    def visible(self, value):
        oid = self._nid.name
        if value:
            cmd = "vis %s,1" % oid
        else:
            cmd = "vis %s,0" % oid
        self._send(cmd)


class IHeightable(NxInterface):
    @property
    def height(self):
        return self._get_nex_number_property("hig", False, 32)

    @height.setter
    def height(self, value):
        self._set_nex_number_property("hig", value)


class IWidthable(NxInterface):
    @property
    def width(self):
        return self._get_nex_number_property("wid", False, 32)

    @width.setter
    def width(self, value):
        self._set_nex_number_property("wid", value)


class ITouchable(NxInterface):
    _callback = None

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, func):
        print("set callback %s" % func)
        self._callback = func

    def process_event(self, pid, cid, event_type):
        assert isinstance(event_type, Event.Touch)

        if pid != self._nid.pid:
            return False

        if cid != self._nid.cid:
            return False

        if event_type in [Event.Touch.Press, Event.Touch.Release]:
            if self.callback is not None:
                self.callback(self, event_type)
                return True

        return False
