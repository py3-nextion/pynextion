from collections import OrderedDict
from .objects import (
    PID_DEFAULT
)
from .widgets import NexPage
from .exceptions import NexException, NexIdException, NexNameException
from .factory import WidgetFactory


class NexComponents:
    def __init__(self, nexserial):
        self.nexserial = nexserial
        self.D_PAGES_BY_NAME = OrderedDict()
        self.D_PAGES_BY_PID = OrderedDict()

    def hook_page(self, name, pid=PID_DEFAULT):
        if name in self.D_PAGES_BY_NAME.keys():
            raise NexNameException("name (%s) must be unique" % name)
        if pid in self.D_PAGES_BY_PID.keys():
            raise NexIdException("pid (%s) must be unique" % pid)
        nexpage = NexPage(self.nexserial, name, pid)
        self.D_PAGES_BY_NAME[name] = nexpage
        self.D_PAGES_BY_PID[pid] = nexpage
        return nexpage

    def page(self, name=None, pid=None):
        if name is not None and pid is None:
            return self.D_PAGES_BY_NAME[name]
        elif name is None and pid is not None:
            return self.D_PAGES_BY_PID[pid]
        elif name is not None and pid is not None:
            raise NexException("name and pid shouldn't be defined both")
        else:
            raise NexException("name or pid should be defined")

    @property
    def pages(self):
        for name, page in self.D_PAGES_BY_NAME.items():
            yield page

    def read_list(self, data):
        for d_page in data:
            pagename = d_page['name']
            if 'pid' in d_page:
                pid = d_page['pid']
            else:
                pid = PID_DEFAULT
            page = self.hook_page(pagename, pid=pid)
            for d_component in d_page['components']:
                typ = d_component['type']
                name = d_component['name']
                cid = d_component['cid']
                widget_type = WidgetFactory.type(typ)
                page.hook_widget(widget_type, name, cid=cid)

    def to_list(self):
        data = []
        for pagename, page in self.D_PAGES_BY_NAME.items():
            data.append(page.to_dict())
        return data

    def read_json(self, path_or_buf):
        raise NotImplementedError()
