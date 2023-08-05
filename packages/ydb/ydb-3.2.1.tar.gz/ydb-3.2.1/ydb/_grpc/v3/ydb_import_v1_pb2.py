# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ydb_import_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ydb._grpc.v3.protos import ydb_import_pb2 as protos_dot_ydb__import__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ydb_import_v1.proto',
  package='Ydb.Import.V1',
  syntax='proto3',
  serialized_options=b'\n\023tech.ydb.import_.v1Z5github.com/ydb-platform/ydb-go-genproto/Ydb_Import_V1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13ydb_import_v1.proto\x12\rYdb.Import.V1\x1a\x17protos/ydb_import.proto2\xaf\x01\n\rImportService\x12Q\n\x0cImportFromS3\x12\x1f.Ydb.Import.ImportFromS3Request\x1a .Ydb.Import.ImportFromS3Response\x12K\n\nImportData\x12\x1d.Ydb.Import.ImportDataRequest\x1a\x1e.Ydb.Import.ImportDataResponseBL\n\x13tech.ydb.import_.v1Z5github.com/ydb-platform/ydb-go-genproto/Ydb_Import_V1b\x06proto3'
  ,
  dependencies=[protos_dot_ydb__import__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_IMPORTSERVICE = _descriptor.ServiceDescriptor(
  name='ImportService',
  full_name='Ydb.Import.V1.ImportService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=64,
  serialized_end=239,
  methods=[
  _descriptor.MethodDescriptor(
    name='ImportFromS3',
    full_name='Ydb.Import.V1.ImportService.ImportFromS3',
    index=0,
    containing_service=None,
    input_type=protos_dot_ydb__import__pb2._IMPORTFROMS3REQUEST,
    output_type=protos_dot_ydb__import__pb2._IMPORTFROMS3RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ImportData',
    full_name='Ydb.Import.V1.ImportService.ImportData',
    index=1,
    containing_service=None,
    input_type=protos_dot_ydb__import__pb2._IMPORTDATAREQUEST,
    output_type=protos_dot_ydb__import__pb2._IMPORTDATARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_IMPORTSERVICE)

DESCRIPTOR.services_by_name['ImportService'] = _IMPORTSERVICE

# @@protoc_insertion_point(module_scope)
