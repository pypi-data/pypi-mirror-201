import sys

import google.protobuf
from packaging.version import Version
from ... import _utilities

# generated files are incompatible between 3 and 4 protobuf versions
# import right generated version for current protobuf lib
# sdk code must always import from ydb._grpc.common
protobuf_version = Version(google.protobuf.__version__)

# for compatible with arcadia
if _utilities.check_module_exists("ydb.public.api"):
    from ydb.public.api.grpc import *  # noqa

    sys.modules["ydb._grpc.common"] = sys.modules["ydb.public.api.grpc"]

    from ydb.public.api import protos

    sys.modules["ydb._grpc.common.protos"] = sys.modules["ydb.public.api.protos"]
else:
    # common way, outside of arcadia
    if protobuf_version < Version("4.0"):
        from ydb._grpc.v3 import *  # noqa

        sys.modules["ydb._grpc.common"] = sys.modules["ydb._grpc.v3"]

        from ydb._grpc.v3 import protos  # noqa

        sys.modules["ydb._grpc.common.protos"] = sys.modules["ydb._grpc.v3.protos"]
    else:
        from ydb._grpc.v4 import *  # noqa

        sys.modules["ydb._grpc.common"] = sys.modules["ydb._grpc.v4"]

        from ydb._grpc.v4 import protos  # noqa

        sys.modules["ydb._grpc.common.protos"] = sys.modules["ydb._grpc.v4.protos"]
