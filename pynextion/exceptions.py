class AbstractNexException(Exception):
    pass


class NexMessageException(AbstractNexException):
    pass


class NexMessageLengthException(NexMessageException):
    pass


class NexMessageEndException(NexMessageException):
    pass


class NexMessageFirstByteException(NexMessageException):
    pass


class NexComponentException(AbstractNexException):
    pass


class NexComponentNameException(AbstractNexException):
    pass


class NexComponentIdException(AbstractNexException):
    pass
