from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RawMeteoData(_message.Message):
    __slots__ = ["datetime", "humidity", "temperature"]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    datetime: _timestamp_pb2.Timestamp
    humidity: float
    temperature: float
    def __init__(self, temperature: _Optional[float] = ..., humidity: _Optional[float] = ..., datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RawPollutionData(_message.Message):
    __slots__ = ["co2", "datetime"]
    CO2_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    co2: int
    datetime: _timestamp_pb2.Timestamp
    def __init__(self, co2: _Optional[int] = ..., datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
