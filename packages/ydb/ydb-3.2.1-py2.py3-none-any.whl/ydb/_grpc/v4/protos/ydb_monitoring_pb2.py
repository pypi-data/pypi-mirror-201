# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/ydb_monitoring.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ydb._grpc.v4.protos import ydb_operation_pb2 as protos_dot_ydb__operation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bprotos/ydb_monitoring.proto\x12\x0eYdb.Monitoring\x1a\x1aprotos/ydb_operation.proto\"g\n\nStatusFlag\"Y\n\x06Status\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04GREY\x10\x01\x12\t\n\x05GREEN\x10\x02\x12\x08\n\x04\x42LUE\x10\x03\x12\n\n\x06YELLOW\x10\x04\x12\n\n\x06ORANGE\x10\x05\x12\x07\n\x03RED\x10\x06\"\xbe\x01\n\x10SelfCheckRequest\x12\x39\n\x10operation_params\x18\x01 \x01(\x0b\x32\x1f.Ydb.Operations.OperationParams\x12\x1d\n\x15return_verbose_status\x18\x02 \x01(\x08\x12\x39\n\x0eminimum_status\x18\x03 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x15\n\rmaximum_level\x18\x04 \x01(\r\"A\n\x11SelfCheckResponse\x12,\n\toperation\x18\x01 \x01(\x0b\x32\x19.Ydb.Operations.Operation\"M\n\x10NodeCheckRequest\x12\x39\n\x10operation_params\x18\x01 \x01(\x0b\x32\x1f.Ydb.Operations.OperationParams\"A\n\x11NodeCheckResponse\x12,\n\toperation\x18\x01 \x01(\x0b\x32\x19.Ydb.Operations.Operation\"g\n\tSelfCheck\"Z\n\x06Result\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x08\n\x04GOOD\x10\x01\x12\x0c\n\x08\x44\x45GRADED\x10\x02\x12\x18\n\x14MAINTENANCE_REQUIRED\x10\x03\x12\r\n\tEMERGENCY\x10\x04\"T\n\x12StoragePDiskStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x32\n\x07overall\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\"\xc0\x01\n\x12StorageVDiskStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x32\n\x07overall\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x37\n\x0cvdisk_status\x18\x03 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x31\n\x05pdisk\x18\x04 \x01(\x0b\x32\".Ydb.Monitoring.StoragePDiskStatus\"\x88\x01\n\x12StorageGroupStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x32\n\x07overall\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x32\n\x06vdisks\x18\x03 \x03(\x0b\x32\".Ydb.Monitoring.StorageVDiskStatus\"\x87\x01\n\x11StoragePoolStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x32\n\x07overall\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x32\n\x06groups\x18\x03 \x03(\x0b\x32\".Ydb.Monitoring.StorageGroupStatus\"u\n\rStorageStatus\x12\x32\n\x07overall\x18\x01 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x30\n\x05pools\x18\x02 \x03(\x0b\x32!.Ydb.Monitoring.StoragePoolStatus\"\x81\x01\n\x13\x43omputeTabletStatus\x12\x32\n\x07overall\x18\x01 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\r\n\x05\x63ount\x18\x04 \x01(\r\x12\n\n\x02id\x18\x05 \x03(\t\"c\n\x10ThreadPoolStatus\x12\x32\n\x07overall\x18\x01 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05usage\x18\x03 \x01(\x02\"d\n\x11LoadAverageStatus\x12\x32\n\x07overall\x18\x01 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x0c\n\x04load\x18\x02 \x01(\x02\x12\r\n\x05\x63ores\x18\x03 \x01(\r\"\xeb\x01\n\x11\x43omputeNodeStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x32\n\x07overall\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x34\n\x07tablets\x18\x03 \x03(\x0b\x32#.Ydb.Monitoring.ComputeTabletStatus\x12/\n\x05pools\x18\x04 \x03(\x0b\x32 .Ydb.Monitoring.ThreadPoolStatus\x12/\n\x04load\x18\x05 \x01(\x0b\x32!.Ydb.Monitoring.LoadAverageStatus\"\xab\x01\n\rComputeStatus\x12\x32\n\x07overall\x18\x01 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x30\n\x05nodes\x18\x02 \x03(\x0b\x32!.Ydb.Monitoring.ComputeNodeStatus\x12\x34\n\x07tablets\x18\x03 \x03(\x0b\x32#.Ydb.Monitoring.ComputeTabletStatus\"6\n\x0cLocationNode\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04host\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\r\"0\n\x14LocationStoragePDisk\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"W\n\x14LocationStorageVDisk\x12\n\n\x02id\x18\x01 \x03(\t\x12\x33\n\x05pdisk\x18\x02 \x03(\x0b\x32$.Ydb.Monitoring.LocationStoragePDisk\"W\n\x14LocationStorageGroup\x12\n\n\x02id\x18\x01 \x03(\t\x12\x33\n\x05vdisk\x18\x02 \x01(\x0b\x32$.Ydb.Monitoring.LocationStorageVDisk\"X\n\x13LocationStoragePool\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x33\n\x05group\x18\x02 \x01(\x0b\x32$.Ydb.Monitoring.LocationStorageGroup\"p\n\x0fLocationStorage\x12*\n\x04node\x18\x01 \x01(\x0b\x32\x1c.Ydb.Monitoring.LocationNode\x12\x31\n\x04pool\x18\x02 \x01(\x0b\x32#.Ydb.Monitoring.LocationStoragePool\"#\n\x13LocationComputePool\x12\x0c\n\x04name\x18\x01 \x01(\t\"@\n\x15LocationComputeTablet\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x03(\t\x12\r\n\x05\x63ount\x18\x03 \x01(\r\"\xa7\x01\n\x0fLocationCompute\x12*\n\x04node\x18\x01 \x01(\x0b\x32\x1c.Ydb.Monitoring.LocationNode\x12\x31\n\x04pool\x18\x02 \x01(\x0b\x32#.Ydb.Monitoring.LocationComputePool\x12\x35\n\x06tablet\x18\x03 \x01(\x0b\x32%.Ydb.Monitoring.LocationComputeTablet\" \n\x10LocationDatabase\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xa2\x01\n\x08Location\x12\x30\n\x07storage\x18\x01 \x01(\x0b\x32\x1f.Ydb.Monitoring.LocationStorage\x12\x30\n\x07\x63ompute\x18\x02 \x01(\x0b\x32\x1f.Ydb.Monitoring.LocationCompute\x12\x32\n\x08\x64\x61tabase\x18\x03 \x01(\x0b\x32 .Ydb.Monitoring.LocationDatabase\"\xd2\x01\n\x08IssueLog\x12\n\n\x02id\x18\x01 \x01(\t\x12\x31\n\x06status\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12\x0f\n\x07message\x18\x03 \x01(\t\x12*\n\x08location\x18\x04 \x01(\x0b\x32\x18.Ydb.Monitoring.Location\x12\x0e\n\x06reason\x18\x05 \x03(\t\x12\x0c\n\x04type\x18\x06 \x01(\t\x12\r\n\x05level\x18\x07 \x01(\r\x12\x0e\n\x06listed\x18\x08 \x01(\r\x12\r\n\x05\x63ount\x18\t \x01(\r\"\xb2\x01\n\x0e\x44\x61tabaseStatus\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x32\n\x07overall\x18\x02 \x01(\x0e\x32!.Ydb.Monitoring.StatusFlag.Status\x12.\n\x07storage\x18\x03 \x01(\x0b\x32\x1d.Ydb.Monitoring.StorageStatus\x12.\n\x07\x63ompute\x18\x04 \x01(\x0b\x32\x1d.Ydb.Monitoring.ComputeStatus\"\xb4\x01\n\x0fSelfCheckResult\x12;\n\x11self_check_result\x18\x01 \x01(\x0e\x32 .Ydb.Monitoring.SelfCheck.Result\x12+\n\tissue_log\x18\x02 \x03(\x0b\x32\x18.Ydb.Monitoring.IssueLog\x12\x37\n\x0f\x64\x61tabase_status\x18\x03 \x03(\x0b\x32\x1e.Ydb.Monitoring.DatabaseStatusBi\n\x13tech.ydb.monitoringB\x10MonitoringProtosZ=github.com/ydb-platform/ydb-go-genproto/protos/Ydb_Monitoring\xf8\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.ydb_monitoring_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023tech.ydb.monitoringB\020MonitoringProtosZ=github.com/ydb-platform/ydb-go-genproto/protos/Ydb_Monitoring\370\001\001'
  _STATUSFLAG._serialized_start=75
  _STATUSFLAG._serialized_end=178
  _STATUSFLAG_STATUS._serialized_start=89
  _STATUSFLAG_STATUS._serialized_end=178
  _SELFCHECKREQUEST._serialized_start=181
  _SELFCHECKREQUEST._serialized_end=371
  _SELFCHECKRESPONSE._serialized_start=373
  _SELFCHECKRESPONSE._serialized_end=438
  _NODECHECKREQUEST._serialized_start=440
  _NODECHECKREQUEST._serialized_end=517
  _NODECHECKRESPONSE._serialized_start=519
  _NODECHECKRESPONSE._serialized_end=584
  _SELFCHECK._serialized_start=586
  _SELFCHECK._serialized_end=689
  _SELFCHECK_RESULT._serialized_start=599
  _SELFCHECK_RESULT._serialized_end=689
  _STORAGEPDISKSTATUS._serialized_start=691
  _STORAGEPDISKSTATUS._serialized_end=775
  _STORAGEVDISKSTATUS._serialized_start=778
  _STORAGEVDISKSTATUS._serialized_end=970
  _STORAGEGROUPSTATUS._serialized_start=973
  _STORAGEGROUPSTATUS._serialized_end=1109
  _STORAGEPOOLSTATUS._serialized_start=1112
  _STORAGEPOOLSTATUS._serialized_end=1247
  _STORAGESTATUS._serialized_start=1249
  _STORAGESTATUS._serialized_end=1366
  _COMPUTETABLETSTATUS._serialized_start=1369
  _COMPUTETABLETSTATUS._serialized_end=1498
  _THREADPOOLSTATUS._serialized_start=1500
  _THREADPOOLSTATUS._serialized_end=1599
  _LOADAVERAGESTATUS._serialized_start=1601
  _LOADAVERAGESTATUS._serialized_end=1701
  _COMPUTENODESTATUS._serialized_start=1704
  _COMPUTENODESTATUS._serialized_end=1939
  _COMPUTESTATUS._serialized_start=1942
  _COMPUTESTATUS._serialized_end=2113
  _LOCATIONNODE._serialized_start=2115
  _LOCATIONNODE._serialized_end=2169
  _LOCATIONSTORAGEPDISK._serialized_start=2171
  _LOCATIONSTORAGEPDISK._serialized_end=2219
  _LOCATIONSTORAGEVDISK._serialized_start=2221
  _LOCATIONSTORAGEVDISK._serialized_end=2308
  _LOCATIONSTORAGEGROUP._serialized_start=2310
  _LOCATIONSTORAGEGROUP._serialized_end=2397
  _LOCATIONSTORAGEPOOL._serialized_start=2399
  _LOCATIONSTORAGEPOOL._serialized_end=2487
  _LOCATIONSTORAGE._serialized_start=2489
  _LOCATIONSTORAGE._serialized_end=2601
  _LOCATIONCOMPUTEPOOL._serialized_start=2603
  _LOCATIONCOMPUTEPOOL._serialized_end=2638
  _LOCATIONCOMPUTETABLET._serialized_start=2640
  _LOCATIONCOMPUTETABLET._serialized_end=2704
  _LOCATIONCOMPUTE._serialized_start=2707
  _LOCATIONCOMPUTE._serialized_end=2874
  _LOCATIONDATABASE._serialized_start=2876
  _LOCATIONDATABASE._serialized_end=2908
  _LOCATION._serialized_start=2911
  _LOCATION._serialized_end=3073
  _ISSUELOG._serialized_start=3076
  _ISSUELOG._serialized_end=3286
  _DATABASESTATUS._serialized_start=3289
  _DATABASESTATUS._serialized_end=3467
  _SELFCHECKRESULT._serialized_start=3470
  _SELFCHECKRESULT._serialized_end=3650
# @@protoc_insertion_point(module_scope)
