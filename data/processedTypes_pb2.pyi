from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pollution(_message.Message):
    __slots__ = ["datetime", "pollution"]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    POLLUTION_FIELD_NUMBER: _ClassVar[int]
    datetime: _timestamp_pb2.Timestamp
    pollution: float
    def __init__(self, pollution: _Optional[float] = ..., datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Wellness(_message.Message):
    __slots__ = ["datetime", "wellness"]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    WELLNESS_FIELD_NUMBER: _ClassVar[int]
    datetime: _timestamp_pb2.Timestamp
    wellness: float
    def __init__(self, wellness: _Optional[float] = ..., datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
