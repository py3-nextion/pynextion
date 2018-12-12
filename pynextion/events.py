from enum import Enum
import ctypes
from .constants import Return
from .exceptions import (
    NexMessageException,
    NexMessageEndException,
    NexMessageLengthException,
    NexMessageFirstByteException
)


class Event:
    class Touch(Enum):
        Press = 0x01
        Release = 0x00


def hex_disp(msg):
    return ''.join(['0x%x ' % b for b in msg])


def has_end(msg):
    return msg[-1] == 0xff and msg[-2] == 0xff and msg[-3] == 0xff


def ensure_has_end(msg):
    if not has_end(msg):
        raise NexMessageEndException("Message %r must end with 0xff 0xff 0xff" % msg)


class AbstractMsgEvent:
    EXPECTED_LENGTH = None
    FIRST_BYTE = None

    @classmethod
    def ensure_has_expected_length(cls, msg):
        expected_length = cls.EXPECTED_LENGTH
        n = len(msg)
        if expected_length is not None and n != expected_length:
            raise NexMessageLengthException("Event message %r must have %d bytes not %d" % (msg, expected_length, n))

    @classmethod
    def ensure_has_expected_first_byte(cls, msg, first_byte):
        expected_first_byte = cls.FIRST_BYTE
        if first_byte != expected_first_byte:
            raise NexMessageFirstByteException("Event message %r must have %d as first byte not %d" % (msg, expected_first_byte, first_byte))
    
    def isempty(self):
        return False

    def issuccess(self):
        return True


class TouchEvent(AbstractMsgEvent):
    EXPECTED_LENGTH = 7
    FIRST_BYTE = Return.Code.EVENT_TOUCH_HEAD

    code = None
    pid = None
    cid = None
    tevts = None

    def __init__(self, code, pid, cid, tevts):
        self.code = code
        self.pid = pid
        self.cid = cid
        self.tevts = tevts

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        pid = int(msg[1])
        cid = int(msg[2])
        tevts = Event.Touch(msg[3])
        return TouchEvent(code, pid, cid, tevts)


class CurrentPageIDHeadEvent(AbstractMsgEvent):
    EXPECTED_LENGTH = 5
    FIRST_BYTE = Return.Code.CURRENT_PAGE_ID_HEAD

    code = None
    pid = None

    def __init__(self, code, pid):
        self.code = code
        self.pid = pid

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        pid = int(msg[1])
        return CurrentPageIDHeadEvent(code, pid)


class PositionHeadEvent(AbstractMsgEvent):
    EXPECTED_LENGTH = 9
    FIRST_BYTE = Return.Code.EVENT_POSITION_HEAD

    code = None
    x = None
    y = None
    tevts = None

    def __init__(self, code, x, y, tevts):
        self.code = code
        self.x = x
        self.y = y
        self.tevts = tevts

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        x = (msg[1] << 8) + msg[2]
        y = (msg[3] << 8) + msg[4]
        tevts = Event.Touch(msg[5])
        return PositionHeadEvent(code, x, y, tevts)


class SleepPositionHeadEvent(AbstractMsgEvent):
    EXPECTED_LENGTH = 9
    FIRST_BYTE = Return.Code.EVENT_SLEEP_POSITION_HEAD

    code = None
    x = None
    y = None
    tevts = None

    def __init__(self, code, x, y, tevts):
        self.code = code
        self.x = x
        self.y = y
        self.tevts = tevts

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        x = (msg[1] << 8) + msg[2]
        y = (msg[3] << 8) + msg[4]
        tevts = Event.Touch(msg[5])
        return SleepPositionHeadEvent(code, x, y, tevts)


class StringHeadEvent(AbstractMsgEvent):
    EXPECTED_LENGTH = None
    FIRST_BYTE = Return.Code.STRING_HEAD

    code = None
    value = None

    def __init__(self, code, value):
        self.code = code
        self.value = value

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        value = bytearray(msg[1:-3]).decode("utf-8")
        return StringHeadEvent(code, value)


class NumberHeadEvent(AbstractMsgEvent):
    EXPECTED_LENGTH = 8
    FIRST_BYTE = Return.Code.NUMBER_HEAD

    code = None
    value = None
    signed_value = None

    def __init__(self, code, value, signed_value):
        self.code = code
        self.value = value
        self.signed_value = signed_value

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        value = msg[1] + (msg[2] << 8) + (msg[3] << 16) + (msg[4] << 24)
        signed_value = ctypes.c_int32(value).value
        return NumberHeadEvent(code, value, signed_value)


class CommandSucceeded(AbstractMsgEvent):
    EXPECTED_LENGTH = 4
    FIRST_BYTE = Return.Code.CMD_FINISHED

    @classmethod
    def parse(cls, msg):
        ensure_has_end(msg)
        cls.ensure_has_expected_length(msg)
        code = Return.Code(msg[0])
        cls.ensure_has_expected_first_byte(msg, code)
        return CommandSucceeded()


class EmptyMessage(AbstractMsgEvent):
    EXPECTED_LENGTH = 0
    FIRST_BYTE = None

    def __init__(self):
        pass

    def issuccess(self):
        return False

    def isempty(self):
        return True


D_BYTE0_EVENT = {
    Return.Code.CMD_FINISHED.value: CommandSucceeded,
    Return.Code.EVENT_TOUCH_HEAD.value: TouchEvent,
    Return.Code.CURRENT_PAGE_ID_HEAD.value: CurrentPageIDHeadEvent,
    Return.Code.EVENT_POSITION_HEAD.value: PositionHeadEvent,
    Return.Code.EVENT_SLEEP_POSITION_HEAD.value: SleepPositionHeadEvent,
    Return.Code.STRING_HEAD.value: StringHeadEvent,
    Return.Code.NUMBER_HEAD.value: NumberHeadEvent
}


NEX_EXCEPTIONS = [
    Return.Code.INVALID_CMD,
    Return.Code.CMD_FINISHED,
    Return.Code.INVALID_COMPONENT_ID,
    Return.Code.INVALID_PAGE_ID,
    Return.Code.INVALID_PICTURE_ID,
    Return.Code.INVALID_FONT_ID,
    Return.Code.INVALID_BAUD,
    Return.Code.INVALID_VARIABLE,
    Return.Code.INVALID_OPERATION,
    Return.Code.INVALID_ASSIGN,
    Return.Code.INVALID_EEPROM,
    Return.Code.INVALID_PARAMETER_QUANTITY,
    Return.Code.INVALID_IO,
    Return.Code.INVALID_ESC_CHAR,
    Return.Code.INVALID_VAR_NAME_TOO_LONG
]


class MsgEvent():
    @classmethod
    def parse(cls, msg):
        if len(msg) == 0:
            return EmptyMessage()
        else:
            first_byte = msg[0]
            if first_byte in D_BYTE0_EVENT:
                evt_typ = D_BYTE0_EVENT[first_byte]
                return evt_typ.parse(msg)
            else:
                code = Return.Code(first_byte)
                if code in NEX_EXCEPTIONS:
                    raise NexMessageException(code)
                else:
                    return NotImplementedError()
