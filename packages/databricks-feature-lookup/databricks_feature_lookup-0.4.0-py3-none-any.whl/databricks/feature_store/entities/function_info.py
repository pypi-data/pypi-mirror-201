from databricks.feature_store.entities._feature_store_object import _FeatureStoreObject
from databricks.feature_store.protos.feature_spec_pb2 import (
    FunctionInfo as ProtoFunctionInfo,
)


class FunctionInfo(_FeatureStoreObject):
    def __init__(self, udf_name: str, md5: str):
        if not udf_name:
            raise ValueError("udf_name must be non-empty.")
        if not md5:
            raise ValueError("md5 must be non-empty.")
        self._udf_name = udf_name
        self._md5 = md5

    @property
    def udf_name(self) -> str:
        return self._udf_name

    @property
    def md5(self) -> str:
        return self._md5

    @classmethod
    def from_proto(cls, function_info_proto):
        return cls(udf_name=function_info_proto.udf_name, md5=function_info_proto.md5)

    def to_proto(self):
        return ProtoFunctionInfo(udf_name=self.udf_name, md5=self.md5)
