from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Connection(_message.Message):
    __slots__ = ["port"]
    PORT_FIELD_NUMBER: _ClassVar[int]
    port: int
    def __init__(self, port: _Optional[int] = ...) -> None: ...

class Pollution(_message.Message):
    __slots__ = ["pollution"]
    POLLUTION_FIELD_NUMBER: _ClassVar[int]
    pollution: float
    def __init__(self, pollution: _Optional[float] = ...) -> None: ...

class Wellness(_message.Message):
    __slots__ = ["wellness"]
    WELLNESS_FIELD_NUMBER: _ClassVar[int]
    wellness: float
    def __init__(self, wellness: _Optional[float] = ...) -> None: ...
