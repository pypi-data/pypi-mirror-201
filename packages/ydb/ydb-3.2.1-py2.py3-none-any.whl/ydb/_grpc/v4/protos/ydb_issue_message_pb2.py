# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/ydb_issue_message.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eprotos/ydb_issue_message.proto\x12\tYdb.Issue\"\x91\x02\n\x0cIssueMessage\x12\x32\n\x08position\x18\x01 \x01(\x0b\x32 .Ydb.Issue.IssueMessage.Position\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x36\n\x0c\x65nd_position\x18\x03 \x01(\x0b\x32 .Ydb.Issue.IssueMessage.Position\x12\x12\n\nissue_code\x18\x04 \x01(\r\x12\x10\n\x08severity\x18\x05 \x01(\r\x12\'\n\x06issues\x18\x06 \x03(\x0b\x32\x17.Ydb.Issue.IssueMessage\x1a\x35\n\x08Position\x12\x0b\n\x03row\x18\x01 \x01(\r\x12\x0e\n\x06\x63olumn\x18\x02 \x01(\r\x12\x0c\n\x04\x66ile\x18\x03 \x01(\tBG\n\x08tech.ydbZ8github.com/ydb-platform/ydb-go-genproto/protos/Ydb_Issue\xf8\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.ydb_issue_message_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\010tech.ydbZ8github.com/ydb-platform/ydb-go-genproto/protos/Ydb_Issue\370\001\001'
  _ISSUEMESSAGE._serialized_start=46
  _ISSUEMESSAGE._serialized_end=319
  _ISSUEMESSAGE_POSITION._serialized_start=266
  _ISSUEMESSAGE_POSITION._serialized_end=319
# @@protoc_insertion_point(module_scope)
