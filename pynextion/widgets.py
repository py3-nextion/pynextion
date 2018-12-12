from collections import OrderedDict

from .objects import (
    IWidget,
    NexId,
    PID_DEFAULT,
    CID_DEFAULT
)

from .interfaces import (
    NxInterface,
    IViewable,
    IBooleanValued,
    INumericalUnsignedValued,
    INumericalSignedValued,
    IStringValued,
    IFontStyleable,
    IColourable,
    IPicturable,
    ITouchable,
    IWidthable,
    IHeightable
)

from .exceptions import (
    NexComponentException,
    NexComponentNameException,
    NexComponentIdException
)


class NexButton(IWidget, IViewable, IStringValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexCheckbox(IWidget, IViewable, IBooleanValued, IColourable, ITouchable):
    pass


class NexCrop(IWidget, IViewable, IPicturable, ITouchable):
    pass


class NexDualStateButton(IWidget, IViewable, IBooleanValued, IColourable, ITouchable):
    pass


class NexGauge(IWidget, IViewable, INumericalUnsignedValued, IColourable, ITouchable):
    pass


class NexHotspot(IWidget, ITouchable):
    pass


class NexNumber(IWidget, IViewable, INumericalSignedValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexPage(IWidget):
    def __init__(self, nexserial, name, pid=PID_DEFAULT, cid=CID_DEFAULT):
        self._nid = NexId(nexserial, name, pid, cid)
        self.D_WIDGETS_BY_NAME = OrderedDict()
        self.D_WIDGETS_BY_CID = OrderedDict()

    def show(self):
        return self._show_by_name()

    def _show_by_id(self):
        oid = self._nid.pid
        return self._nid._nexserial.send("page %s" % oid)

    def _show_by_name(self):
        oid = self._nid.name
        return self._nid._nexserial.send("page %s" % oid)

    def ishown(self):
        pid1 = self._nid._nexserial.current_page
        pid2 = self.pid
        return pid1 == pid2

    def hook_widget(self, widget_type, name, cid=CID_DEFAULT):
        pid = self._nid.pid
        if name in self.D_WIDGETS_BY_NAME.keys():
            raise NexComponentNameException("name (%s) must be unique" % name)
        if cid in self.D_WIDGETS_BY_CID.keys():
            raise NexComponentIdException("cid (%s) must be unique" % cid)
        widget = widget_type(self._nid._nexserial, name, pid=pid, cid=cid)
        self.D_WIDGETS_BY_NAME[name] = widget
        self.D_WIDGETS_BY_CID[cid] = widget
        return widget

    def widget(self, name=None, cid=None):
        if name is not None and cid is None:
            return self.D_WIDGETS_BY_NAME[name]
        elif name is None and cid is not None:
            return self.D_WIDGETS_BY_CID[cid]
        elif name is not None and cid is not None:
            raise NexComponentException("name and cid shouldn't be defined both")
        else:
            raise NexComponentException("name or cid should be defined")

    def to_dict(self):
        return {
            "pid": self._nid.pid,
            "name": self._nid.name,
            "components": [widget.to_dict() for widget in self.widgets]
        }

    @property
    def widgets(self):
        for name, widget in self.D_WIDGETS_BY_NAME.items():
            yield widget


class NexPicture(IWidget, IViewable, IPicturable):
    pass


class NexProgressBar(IWidget, IViewable, INumericalUnsignedValued, IColourable, ITouchable):
    pass


class NexQRcode(IWidget, IViewable, IStringValued):
    pass


class NexRadio(IWidget, IViewable, IBooleanValued, IColourable, ITouchable):
    pass


class NexScrollText(IWidget, IViewable, IStringValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexSliderCursor(IWidget, IWidthable, IHeightable):
    def __init__(self, nid):
        self._nid = nid


class NexSlider(IWidget, IViewable, INumericalUnsignedValued, IColourable, ITouchable):
    @property
    def cursor(self):
        return NexSliderCursor(self._nid)


class NexText(IWidget, IViewable, IStringValued, IFontStyleable, IColourable, ITouchable):
    pass


class NexWaveformChannel:
    def __init__(self, nid, chid):
        self._nid = nid
        self._chid = chid  # channel id

    def append(self, value):
        nid = self._nid
        cid = nid.cid
        chid = self._chid
        nexserial = nid._nexserial
        if isinstance(value, list):
            vals = value
            n = len(vals)
            cmd = "addt %s,%s,%s" % (cid, chid, n)
            nexserial.send(cmd)
            nexserial.sp.write(bytearray(vals))
            return nexserial.read_all()
        else:
            if value < 0 or value > 255:
                raise(Exception("value must be in 0-255 range"))
            cmd = "add %s,%s,%s" % (cid, chid, value)
            return nexserial.send(cmd)


class NexWaveformChannels:
    def __init__(self, nid):
        self._nid = nid

    def __getitem__(self, id):
        return NexWaveformChannel(self._nid, id)


class NexWaveformGrid(IWidget, NxInterface):
    def __init__(self, nid):
        self._nid = nid

    @property
    def width(self):
        return self._get_nex_number_property("gdw")

    @width.setter
    def width(self, value):
        self._set_nex_number_property("gdw", value)

    @property
    def height(self):
        return self._get_nex_number_property("gdh")

    @height.setter
    def height(self, value):
        self._set_nex_number_property("gdh", value)

    @property
    def color(self):
        return self._get_nex_number_property("gdc")

    @color.setter
    def color(self, value):
        self._set_nex_number_property("gdc", value)


class NexWaveform(IWidget, IViewable, IColourable, ITouchable):
    @property
    def grid(self):
        return NexWaveformGrid(self._nid)

    @property
    def channels(self):
        return NexWaveformChannels(self._nid)
