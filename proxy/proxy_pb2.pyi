from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import data.processedTypes_pb2 as _processedTypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Result(_message.Message):
    __slots__ = ["datetime", "pollution", "wellness"]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    POLLUTION_FIELD_NUMBER: _ClassVar[int]
    WELLNESS_FIELD_NUMBER: _ClassVar[int]
    datetime: _timestamp_pb2.Timestamp
    pollution: _processedTypes_pb2.Pollution
    wellness: _processedTypes_pb2.Wellness
    def __init__(self, wellness: _Optional[_Union[_processedTypes_pb2.Wellness, _Mapping]] = ..., pollution: _Optional[_Union[_processedTypes_pb2.Pollution, _Mapping]] = ..., datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
