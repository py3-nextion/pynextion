from collections import OrderedDict
from .objects import (
    PID_DEFAULT
)
from .widgets import NexPage
from .exceptions import NexIdException, NexNameException


class NexComponents:
    D_PAGES_BY_NAME = OrderedDict()
    D_PAGES_BY_PID = OrderedDict()

    def __init__(self, nexserial):
        self.nexserial = nexserial

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
            raise NotImplementedError("name and pid shouldn't be defined both")
        else:
            raise NotImplementedError("name or pid should be defined")

    @property
    def pages(self):
        for name, page in self.D_PAGES_BY_NAME.items():
            yield page

    def read_list(data):
        raise NotImplementedError()

    def read_json(path_or_buf):
        raise NotImplementedError()
