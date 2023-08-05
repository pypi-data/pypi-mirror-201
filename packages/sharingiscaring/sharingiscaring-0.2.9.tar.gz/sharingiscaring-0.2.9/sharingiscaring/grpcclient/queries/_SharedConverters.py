from __future__ import annotations
from typing import Protocol
from sharingiscaring.GRPCClient.types_pb2 import *
import base58
import base64
import datetime as dt
from datetime import timezone
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
from sharingiscaring.GRPCClient.CCD_Types import *
from google._upb._message import RepeatedCompositeContainer


class OpenStatusEnum(Enum):
    openForAll = 0
    closedForNew = 1
    closedForAll = 2


class TransactionType(Enum):
    DEPLOY_MODULE = 0
    INIT_CONTRACT = 1
    UPDATE = 2
    TRANSFER = 3
    ADD_BAKER = 4
    REMOVE_BAKER = 5
    UPDATE_BAKER_STAKE = 6
    UPDATE_BAKER_RESTAKE_EARNINGS = 7
    UPDATE_BAKER_KEYS = 8
    UPDATE_CREDENTIAL_KEYS = 9
    ENCRYPTED_AMOUNT_TRANSFER = 10
    TRANSFER_TO_ENCRYPTED = 11
    TRANSFER_TO_PUBLIC = 12
    TRANSFER_WITH_SCHEDULE = 13
    UPDATE_CREDENTIALS = 14
    REGISTER_DATA = 15
    TRANSFER_WITH_MEMO = 16
    ENCRYPTED_AMOUNT_TRANSFER_WITH_MEMO = 17
    TRANSFER_WITH_SCHEDULE_AND_MEMO = 18
    CONFIGURE_BAKER = 19
    CONFIGURE_DELEGATION = 20


class Mixin(Protocol):
    # These types should be encoded to HEX
    bytes_to_hex_types = [
        bytes,
        BlockHash,
        TransactionHash,
        CredentialRegistrationId,
        StateHash,
        Memo,
        ModuleRef,
        Commitment,
        EncryptionKey,
        EncryptedAmount,
        BakerElectionVerifyKey,
        BakerSignatureVerifyKey,
        BakerAggregationVerifyKey,
        RegisteredData,
        IpInfo.IpVerifyKey,
        IpInfo.IpCdiVerifyKey,
        ArInfo.ArPublicKey,
        LeadershipElectionNonce,
        Parameter,
        Sha256Hash,
        ContractStateV0,
        VersionedModuleSource.ModuleSourceV0,
        VersionedModuleSource.ModuleSourceV1,
    ]
    # These types should be shown as is (from the .value property)
    value_property_types = [
        AbsoluteBlockHeight,
        Amount,
        AccountThreshold,
        AccountIndex,
        ArInfo.ArIdentity,
        ArThreshold,
        CredentialsPerBlockLimit,
        BlockHeight,
        BlockItemSummary.TransactionIndex,
        DurationSeconds,
        Energy,
        RewardPeriodLength,
        Epoch,
        InitName,
        IpIdentity,
        IdentityProviderIdentity,
        GenesisIndex,
        ReceiveName,
        SequenceNumber,
        SignatureThreshold,
        Slot,
        TransactionTime,
        UpdateKeysThreshold,
    ]
    # These types need special attention for conversion
    remaining_types = [
        AccountAddress,
        Address,
        AccountVerifyKey,
        BakerId,
        ChainArData,
        ContractAddress,
        DelegatorId,
        Empty,
        Timestamp,
        ElectionDifficulty,
        str,
        int,
        bool,
        float,
    ]

    # all types that are covered by the `convertType` method.
    simple_types = bytes_to_hex_types + value_property_types + remaining_types

    def get_key_value_from_descriptor(self, descriptor, the_list):
        return descriptor.name, getattr(the_list, descriptor.name)

    def generate_account_identifier_input_from(self, hex_address: str):
        try:
            bin_value = base58.b58decode_check(hex_address)[1:]
            address = AccountAddress(value=bin_value)
            account = AccountIdentifierInput(address=address)
            return account
        except:  # pragma: no cover
            return None

    def generate_account_identifier_input_from_baker_id(self, baker_id: CCD_BakerId):
        try:
            account = AccountIdentifierInput(account_index=AccountIndex(value=baker_id))
            return account
        except:  # pragma: no cover
            return None

    def valueIsEmpty(self, value):
        if type(value) == int:
            return value is None
        else:
            if type(value) == RepeatedCompositeContainer:
                return False
            else:
                if hasattr(value, "DESCRIPTOR"):
                    return MessageToDict(value) == {}
                else:  # pragma: no cover
                    return False

    def generate_block_hash_input_from(self, hex_block_hash: str):
        if hex_block_hash == "last_final":
            return BlockHashInput(last_final={})
        else:
            return BlockHashInput(given=BlockHash(value=bytes.fromhex(hex_block_hash)))

    def generate_instance_info_request_from(
        self, contract_index: int, contract_sub_index: int, hex_block_hash: str
    ):

        return InstanceInfoRequest(
            block_hash=self.generate_block_hash_input_from(hex_block_hash),
            address=ContractAddress(
                **{"index": contract_index, "subindex": contract_sub_index}
            ),
        )

    def generate_module_source_request_from(
        self, module_ref: CCD_ModuleRef, hex_block_hash: str
    ):

        return ModuleSourceRequest(
            block_hash=self.generate_block_hash_input_from(hex_block_hash),
            module_ref=ModuleRef(value=bytes.fromhex(module_ref)),
        )

    def convertList(self, message):
        entries = []

        for list_entry in message:
            entries.append(self.convertType(list_entry))

        return entries

    def convertType(self, value):
        # these types have a property `value` that we need to return unmodified
        if type(value) in self.value_property_types:
            return value.value

        if type(value) == bytes:
            return value.hex()
        # these types have a property `value` that we need to encode as HEX>
        elif type(value) in self.bytes_to_hex_types:
            return value.value.hex()

        elif type(value) in [int, bool, str, float]:
            return value

        elif type(value) == ElectionDifficulty:
            return value.value.parts_per_hundred_thousand / 100_000

        elif type(value) == AmountFraction:
            return value.parts_per_hundred_thousand / 100_000

        elif type(value) == Empty:
            return None  # pragma: no cover

        elif type(value) == Address:
            if MessageToDict(value.account) == {}:
                return CCD_Address(
                    **{"contract": self.convertContractAddress(value.contract)}
                )
            else:
                return CCD_Address(
                    **{"account": self.convertAccountAddress(value.account)}
                )

        elif type(value) == AccountAddress:
            return self.convertAccountAddress(value)

        elif type(value) == BakerId:
            return value.value
            # else:
            #     return None

        elif type(value) == ContractAddress:
            return self.convertContractAddress(value)

        elif type(value) == AccountVerifyKey:
            return value.ed25519_key.hex()

        elif type(value) == ChainArData:
            return value.enc_id_cred_pub_share.hex()

        elif type(value) == Timestamp:
            return dt.datetime.fromtimestamp(
                int(MessageToDict(value)["value"]) / 1_000, tz=timezone.utc
            )

        elif type(value) == DelegatorId:
            return value.id.value

    def convertContractAddress(self, value: ContractAddress) -> CCD_ContractAddress:
        return CCD_ContractAddress(**{"index": value.index, "subindex": value.subindex})

    def convertAccountAddress(self, value: AccountAddress) -> CCD_AccountAddress:
        return base58.b58encode_check(b"\x01" + value.value).decode()

    def convertAmount(self, value: Amount) -> microCCD:
        return value.value

    def convertDelegationTarget(self, message) -> CCD_DelegationTarget:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) == Empty:
                pass
            if type(value) == BakerId:
                if self.valueIsEmpty(value):
                    result["passive_delegation"] = True
                else:
                    # result['passive_delegation'] = False
                    result["baker"] = self.convertType(value)

        return CCD_DelegationTarget(**result)

    def convertCommissionRates(self, value) -> CCD_CommissionRates:
        result = {}
        for descriptor in value.DESCRIPTOR.fields:
            key, val = self.get_key_value_from_descriptor(descriptor, value)
            result[key] = val.parts_per_hundred_thousand / 100_000
        return CCD_CommissionRates(**result)

    def convertRelease(self, message) -> CCD_ReleaseSchedule:
        resulting_dict = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if key == "schedules":
                schedule = []
                for entry in value:
                    entry_dict = {}
                    for descriptor in entry.DESCRIPTOR.fields:
                        key, value = self.get_key_value_from_descriptor(
                            descriptor, entry
                        )

                        if key == "transactions":
                            entry_dict[key] = self.convertList(value)

                        elif type(value) == Timestamp:
                            entry_dict[key] = self.convertType(value)

                        elif type(value) == Amount:
                            entry_dict[key] = self.convertType(value)

                    schedule.append(entry_dict)
                resulting_dict["schedules"] = schedule

            elif type(value) == Amount:
                resulting_dict[key] = self.convertType(value)

        return CCD_ReleaseSchedule(**resulting_dict)

    def convertArInfo(self, message) -> CCD_ArInfo:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in [ArInfo.ArIdentity, ArInfo.ArPublicKey]:
                result[key] = self.convertType(value)

            elif type(value) == Description:
                result[key] = self.convertTypeWithSingleValues(value)

        return CCD_ArInfo(**result)

    def convertIpInfo(self, message) -> CCD_IpInfo:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in [IpIdentity, IpInfo.IpVerifyKey, IpInfo.IpCdiVerifyKey]:
                result[key] = self.convertType(value)

            elif type(value) == Description:
                result[key] = self.convertTypeWithSingleValues(value)

        return CCD_IpInfo(**result)

    def convertBakerPoolInfo(self, message) -> CCD_BakerPoolInfo:
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            if key == "open_status":
                result[key] = OpenStatus(value).name

            elif type(value) == CommissionRates:
                result[key] = self.convertCommissionRates(value)

        return CCD_BakerPoolInfo(**result)

    def convertPoolCurrentPaydayInfo(self, message) -> CCD_CurrentPaydayStatus:
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            result[key] = self.convertType(value)

        return CCD_CurrentPaydayStatus(**result)

    def convertInclusiveRange(self, message) -> CCD_InclusiveRangeAmountFraction:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) == AmountFraction:
                result[key] = self.convertType(value)

        return CCD_InclusiveRangeAmountFraction(**result)

    def convertTypeWithSingleValues(self, message):
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) == InclusiveRangeAmountFraction:
                result[key] = self.convertTypeWithSingleValues(value)

            elif type(value) == Ratio:
                result[key] = CCD_Ratio(
                    **{
                        "numerator": value.numerator,
                        "denominator": value.denominator,
                    }
                )

            elif type(value) == RewardPeriodLength:
                result[key] = self.convertType(value.value)

            elif type(value) == MintRate:
                result[key] = CCD_MintRate(
                    **{"mantissa": value.mantissa, "exponent": value.exponent}
                )
            elif type(value) == BakerId:
                if descriptor.json_name in MessageToDict(message):
                    result[key] = self.convertType(value)
            else:
                result[key] = self.convertType(value)

        return result

    def convertPendingChange_Reduce_Remove(
        self, message
    ) -> CCD_StakePendingChange_Remove:

        return self.convertType(message)

    def convertPendingChange(self, message) -> CCD_StakePendingChange:
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if message.WhichOneof("change") == "reduce" and key == "reduce":
                result[key] = self.convertPendingChange_Reduce_Remove(value)
            elif message.WhichOneof("change") == "remove" and key == "remove":
                result[key] = self.convertPendingChange_Reduce_Remove(value)

        return CCD_StakePendingChange(**result)

    def convertExchangeRate(self, message) -> CCD_ExchangeRate:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == Ratio:
                        result[key] = CCD_Ratio(
                            **{
                                "numerator": value.numerator,
                                "denominator": value.denominator,
                            }
                        )

        return CCD_ExchangeRate(**result)

    def convertUpdatePublicKeys(self, message) -> list[CCD_UpdatePublicKey]:
        keys = []

        for entry in message:
            result = {}
            for descriptor in entry.DESCRIPTOR.fields:
                entry_dict = {}
                key, value = self.get_key_value_from_descriptor(descriptor, entry)

                # TODO: this needs to be decoded to hex still
                if type(value) in self.simple_types:
                    keys.append(self.convertType(value))

        return keys

    def convertHigherLevelKeys(self, message) -> CCD_HigherLevelKeys:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if key == "keys":
                    result[key] = self.convertUpdatePublicKeys(value)

                elif type(value) in self.simple_types:
                    result[key] = self.convertType(value)

        return CCD_HigherLevelKeys(**result)

    def convertAccessPublicKeys(self, message) -> list[CCD_UpdatePublicKey]:
        keys = []

        for entry in message:
            for descriptor in entry.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, entry)

                if type(value) in self.simple_types:
                    keys.append(self.convertType(value))

        return keys

    def convertAccessStructure(self, message) -> CCD_AccessStructure:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if self.valueIsEmpty(value):
                    pass
                else:
                    if key == "access_public_keys":
                        result[key] = self.convertAccessPublicKeys(value)

                    elif type(value) in self.simple_types:
                        result[key] = self.convertType(value)

        return CCD_AccessStructure(**result)

    def convertAuthorizationsV0(self, message) -> CCD_AuthorizationsV0:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if self.valueIsEmpty(value):
                    pass
                else:
                    if key == "keys":
                        result[key] = self.convertUpdatePublicKeys(value)

                    elif type(value) == AccessStructure:
                        result[key] = self.convertAccessStructure(value)

                    elif type(value) in self.simple_types:
                        result[key] = self.convertType(value)

        return CCD_AuthorizationsV0(**result)

    def convertAuthorizationsV1(self, message) -> CCD_AuthorizationsV1:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if self.valueIsEmpty(value):
                    pass
                else:
                    if type(value) == AuthorizationsV0:
                        result[key] = self.convertAuthorizationsV0(value)

                    elif type(value) == AccessStructure:
                        result[key] = self.convertAccessStructure(value)

                    elif type(value) in self.simple_types:
                        result[key] = self.convertType(value)

        return CCD_AuthorizationsV1(**result)

    def convertLevel1Update(self, message) -> CCD_Level1Update:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == HigherLevelKeys:
                        result[key] = self.convertHigherLevelKeys(value)

                    elif type(value) == AuthorizationsV0:
                        result[key] = self.convertAuthorizationsV0(value)

                    elif type(value) == AuthorizationsV1:
                        result[key] = self.convertAuthorizationsV1(value)

        return CCD_Level1Update(**result)

    def convertRootUpdate(self, message) -> CCD_RootUpdate:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == HigherLevelKeys:
                        result[key] = self.convertHigherLevelKeys(value)

                    elif type(value) == AuthorizationsV0:
                        result[key] = self.convertAuthorizationsV0(value)

                    elif type(value) == AuthorizationsV1:
                        result[key] = self.convertAuthorizationsV1(value)

        return CCD_RootUpdate(**result)

    def converCommissionRanges(self, message) -> CCD_CommissionRanges:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_CommissionRanges(**result)

    def convertPoolParametersCpv1(self, message) -> CCD_PoolParametersCpv1:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == CommissionRanges:
                        result[key] = self.converCommissionRanges(value)

                    # elif type(value) in [BakerStakeThreshold, ProtocolUpdate]:
                    #         result[key] = self.convertTypeWithSingleValues(value)

                    elif type(value) in self.simple_types:
                        result[key] = self.convertType(value)

                    elif type(value) in [CapitalBound, LeverageFactor]:
                        result[key] = self.convertTypeWithSingleValues(value)

                    elif type(value) == AmountFraction:
                        result[key] = self.convertType(value)

        return CCD_PoolParametersCpv1(**result)

    def convertElectionDifficulty(self, message) -> CCD_ElectionDifficulty:
        # TODO: no test available
        return message.value.parts_per_hundred_thousand / 100_000

    def convertMintRate(self, message) -> CCD_MintRate:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_MintRate(**result)

    def convertTimeParametersCpv1(self, message) -> CCD_TimeParametersCpv1:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_TimeParametersCpv1(**result)

    def convertCooldownParametersCpv1(self, message) -> CCD_CooldownParametersCpv1:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_CooldownParametersCpv1(**result)

    def convertTransactionFeeDistribution(
        self, message
    ) -> CCD_TransactionFeeDistribution:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_TransactionFeeDistribution(**result)

    def convertGasRewards(self, message) -> CCD_GasRewards:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_GasRewards(**result)

    def convertMintDistributionCpv1(self, message) -> CCD_MintDistributionCpv1:
        # TODO: no test available
        result = self.convertTypeWithSingleValues(message)

        return CCD_MintDistributionCpv1(**result)

    def convertMintDistributionCpv0(self, message) -> CCD_MintDistributionCpv0:
        # TODO: no test available
        if self.valueIsEmpty(message):
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                if self.valueIsEmpty(value):
                    pass
                else:
                    if type(value) == MintRate:
                        result[key] = self.convertMintRate(value)

                    elif type(value) == AmountFraction:
                        result[key] = self.convertType(value)

        return CCD_MintDistributionCpv0(**result)
