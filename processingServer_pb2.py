# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: processingServer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16processingServer.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x1a\n\nConnection\x12\x0c\n\x04port\x18\x01 \x01(\x05\"\x1c\n\x08Wellness\x12\x10\n\x08wellness\x18\x01 \x01(\x02\"\x1e\n\tPollution\x12\x11\n\tpollution\x18\x01 \x01(\x02\x32\x81\x01\n\x15\x44\x61taProcessingService\x12\x32\n\x0bPutWellness\x12\t.Wellness\x1a\x16.google.protobuf.Empty\"\x00\x12\x34\n\x0cPutPollution\x12\n.Pollution\x1a\x16.google.protobuf.Empty\"\x00\x32U\n\x11\x43onnectionService\x12@\n\x17SubscribeToLoadBalancer\x12\x0b.Connection\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'processingServer_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CONNECTION._serialized_start=55
  _CONNECTION._serialized_end=81
  _WELLNESS._serialized_start=83
  _WELLNESS._serialized_end=111
  _POLLUTION._serialized_start=113
  _POLLUTION._serialized_end=143
  _DATAPROCESSINGSERVICE._serialized_start=146
  _DATAPROCESSINGSERVICE._serialized_end=275
  _CONNECTIONSERVICE._serialized_start=277
  _CONNECTIONSERVICE._serialized_end=362
# @@protoc_insertion_point(module_scope)