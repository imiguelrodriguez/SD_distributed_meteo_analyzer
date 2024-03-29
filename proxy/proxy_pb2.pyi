from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Result(_message.Message):
    __slots__ = ["datetime", "pollution", "wellness"]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    POLLUTION_FIELD_NUMBER: _ClassVar[int]
    WELLNESS_FIELD_NUMBER: _ClassVar[int]
    datetime: str
    pollution: float
    wellness: float
    def __init__(self, wellness: _Optional[float] = ..., pollution: _Optional[float] = ..., datetime: _Optional[str] = ...) -> None: ...
