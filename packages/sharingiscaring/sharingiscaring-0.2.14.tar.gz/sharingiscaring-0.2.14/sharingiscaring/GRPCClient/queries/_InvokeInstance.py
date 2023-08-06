from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import os
import sys
from rich import print

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def invoke_instance(
        self: GRPCClient,
        block_hash: str,
        instance: int,
        amount: int,
        entrypoint: str,
        parameter: bytes,
        energy: int,
    ) -> CCD_InvokeInstanceResponse:
        result = {}
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value: InvokeInstanceResponse = self.stub.InvokeInstance(
            request=blockHashInput
        )

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif key == "baker_election_info":
                result[key] = self.convertElectionInfoBaker(value)

        return CCD_ElectionInfo(**result)
