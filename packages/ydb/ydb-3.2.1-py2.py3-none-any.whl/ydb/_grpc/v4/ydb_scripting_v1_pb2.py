# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ydb_scripting_v1.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ydb._grpc.v4.protos import ydb_scripting_pb2 as protos_dot_ydb__scripting__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16ydb_scripting_v1.proto\x12\x10Ydb.Scripting.V1\x1a\x1aprotos/ydb_scripting.proto2\x9a\x02\n\x10ScriptingService\x12Q\n\nExecuteYql\x12 .Ydb.Scripting.ExecuteYqlRequest\x1a!.Ydb.Scripting.ExecuteYqlResponse\x12`\n\x10StreamExecuteYql\x12 .Ydb.Scripting.ExecuteYqlRequest\x1a(.Ydb.Scripting.ExecuteYqlPartialResponse0\x01\x12Q\n\nExplainYql\x12 .Ydb.Scripting.ExplainYqlRequest\x1a!.Ydb.Scripting.ExplainYqlResponseBQ\n\x15tech.ydb.scripting.v1Z8github.com/ydb-platform/ydb-go-genproto/Ydb_Scripting_V1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ydb_scripting_v1_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025tech.ydb.scripting.v1Z8github.com/ydb-platform/ydb-go-genproto/Ydb_Scripting_V1'
  _SCRIPTINGSERVICE._serialized_start=73
  _SCRIPTINGSERVICE._serialized_end=355
# @@protoc_insertion_point(module_scope)
