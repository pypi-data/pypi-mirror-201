from __future__ import annotations
import sys
import os
import asyncio

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
import grpc
import base58
import base64
import datetime as dt
from rich.progress import track
from rich import print
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf import message
import sys
import os
import time


from sharingiscaring.GRPCClient.queries._GetPoolInfo import Mixin as _GetPoolInfo
from sharingiscaring.GRPCClient.queries._GetPoolDelegatorsRewardPeriod import (
    Mixin as _GetPoolDelegatorsRewardPeriod,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegatorsRewardPeriod import (
    Mixin as _GetPassiveDelegatorsRewardPeriod,
)
from sharingiscaring.GRPCClient.queries._GetAccountList import Mixin as _GetAccountList
from sharingiscaring.GRPCClient.queries._GetBakerList import Mixin as _GetBakerList
from sharingiscaring.GRPCClient.queries._GetBlocksAtHeight import (
    Mixin as _GetBlocksAtHeight,
)
from sharingiscaring.GRPCClient.queries._GetFinalizedBlocks import (
    Mixin as _GetFinalizedBlocks,
)
from sharingiscaring.GRPCClient.queries._GetInstanceInfo import (
    Mixin as _GetInstanceInfo,
)
from sharingiscaring.GRPCClient.queries._GetInstanceList import (
    Mixin as _GetInstanceList,
)
from sharingiscaring.GRPCClient.queries._GetAnonymityRevokers import (
    Mixin as _GetAnonymityRevokers,
)
from sharingiscaring.GRPCClient.queries._GetIdentityProviders import (
    Mixin as _GetIdentityProviders,
)
from sharingiscaring.GRPCClient.queries._GetPoolDelegators import (
    Mixin as _GetPoolDelegators,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegators import (
    Mixin as _GetPassiveDelegators,
)
from sharingiscaring.GRPCClient.queries._GetAccountInfo import Mixin as _GetAccountInfo
from sharingiscaring.GRPCClient.queries._GetBlockInfo import Mixin as _GetBlockInfo
from sharingiscaring.GRPCClient.queries._GetElectionInfo import (
    Mixin as _GetElectionInfo,
)
from sharingiscaring.GRPCClient.queries._GetTokenomicsInfo import (
    Mixin as _GetTokenomicsInfo,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegationInfo import (
    Mixin as _GetPassiveDelegationInfo,
)
from sharingiscaring.GRPCClient.queries._GetBlockTransactionEvents import (
    Mixin as _GetBlockTransactionEvents,
)
from sharingiscaring.GRPCClient.queries._GetBlockSpecialEvents import (
    Mixin as _GetBlockSpecialEvents,
)
from sharingiscaring.GRPCClient.queries._GetBlockPendingUpdates import (
    Mixin as _GetBlockPendingUpdates,
)
from sharingiscaring.GRPCClient.queries._GetModuleSource import (
    Mixin as _GetModuleSource,
)
from sharingiscaring.GRPCClient.queries._GetBlockChainParameters import (
    Mixin as _GetBlockChainParameters,
)


class GRPCClient(
    _GetPoolInfo,
    _GetAccountList,
    _GetBakerList,
    _GetInstanceInfo,
    _GetInstanceList,
    _GetFinalizedBlocks,
    _GetBlocksAtHeight,
    _GetIdentityProviders,
    _GetAnonymityRevokers,
    _GetPassiveDelegationInfo,
    _GetPassiveDelegators,
    _GetPoolDelegators,
    _GetPoolDelegatorsRewardPeriod,
    _GetPassiveDelegatorsRewardPeriod,
    _GetAccountInfo,
    _GetBlockInfo,
    _GetElectionInfo,
    _GetBlockTransactionEvents,
    _GetBlockSpecialEvents,
    _GetBlockPendingUpdates,
    _GetTokenomicsInfo,
    _GetModuleSource,
    _GetBlockChainParameters,
):
    def __init__(self, hosts: list(dict) = None):
        self.host_index = 0
        if not hosts:
            self.hosts = [{"host": "localhost", "port": 20000}]
        else:
            self.hosts = hosts
        self.connect()

        # if async_check_connection:
        #     loop = asyncio.get_event_loop()
        #     loop.create_task(self.async_check_connection())
        #     loop.run_forever()

    def connect(self):
        self.channel = grpc.insecure_channel(
            f"{self.hosts[self.host_index]['host']}:{self.hosts[self.host_index]['port']}"
        )
        print(
            f"Connecting on: {self.hosts[self.host_index]['host']}:{self.hosts[self.host_index]['port']}"
        )
        self.stub = QueriesStub(self.channel)

    def check_connection(self, function_name=None):
        connected = False
        while not connected:
            try:
                grpc.channel_ready_future(self.channel).result(timeout=0.05)
                connected = True
                # if function_name:
                #     print(f"{function_name} | {connected=}")

            except grpc.FutureTimeoutError:
                print(
                    f"Timeout for  : {self.hosts[self.host_index]['host']}:{self.hosts[self.host_index]['port']}"
                )
                self.host_index += 1
                if self.host_index == len(self.hosts):
                    self.host_index = 0
                self.connect()

    async def async_check_connection(self):
        while True:
            try:
                grpc.channel_ready_future(self.channel).result(timeout=0.1)
            except grpc.FutureTimeoutError:
                print(
                    f"GRPC Timeout for {self.hosts[self.host_index]['host']}:{self.hosts[self.host_index]['port']}"
                )
                self.host_index += 1
                if self.host_index == len(self.hosts):
                    self.host_index = 0
                self.connect()
            await asyncio.sleep(1)


# grpcclient = GRPCClient()
