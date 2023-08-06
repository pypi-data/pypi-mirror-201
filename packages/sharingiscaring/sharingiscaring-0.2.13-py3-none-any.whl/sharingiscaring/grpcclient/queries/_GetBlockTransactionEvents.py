from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
import os
import sys

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import *
from google.protobuf.json_format import MessageToJson, MessageToDict


class Mixin(_SharedConverters):
    def convertNewRelease(self, message) -> list:
        schedule = []
        for entry in message:
            entry_dict = {}
            for descriptor in entry.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if type(value) in self.simple_types:
                    converted_value = self.convertType(value)
                    if converted_value:
                        entry_dict[key] = converted_value
            schedule.append(CCD_NewRelease(**entry_dict))

        return schedule

    def convertEvents(self, message) -> list:
        events = []
        for entry in message:
            entry_dict = {}
            for descriptor in entry.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if type(value) in self.simple_types:
                    converted_value = self.convertType(value)
                    if converted_value:
                        # entry_dict[key] = converted_value
                        events.append(converted_value)
            # if entry_dict == {}:
            #         pass
            # else:
            #     events.append(entry_dict)

        return events

    def convertInstanceInterruptedEvent(
        self, message
    ) -> CCD_ContractTraceElement_Interrupted:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            if key == "events":
                result[key] = self.convertEvents(value)

        return CCD_ContractTraceElement_Interrupted(**result)

    def convertInstanceUpdatedEvent(self, message) -> CCD_InstanceUpdatedEvent:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            if key == "events":
                result[key] = self.convertEvents(value)

        return CCD_InstanceUpdatedEvent(**result)

    def convertInstanceResumedEvent(self, message) -> CCD_ContractTraceElement_Resumed:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_ContractTraceElement_Resumed(**result)

    def convertInstanceTransferredEvent(
        self, message
    ) -> CCD_ContractTraceElement_Transferred:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_ContractTraceElement_Transferred(**result)

    def convertUpdateEvents(self, message) -> list:
        events = []
        for entry in message:

            for descriptor in entry.DESCRIPTOR.fields:
                entry_dict = {}
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == InstanceUpdatedEvent:
                        entry_dict[key] = self.convertInstanceUpdatedEvent(value)

                    if type(value) == ContractTraceElement.Interrupted:
                        entry_dict[key] = self.convertInstanceInterruptedEvent(value)

                    if type(value) == ContractTraceElement.Resumed:
                        entry_dict[key] = self.convertInstanceResumedEvent(value)

                    if type(value) == ContractTraceElement.Transferred:
                        entry_dict[key] = self.convertInstanceTransferredEvent(value)

                if entry_dict == {}:
                    pass
                else:
                    events.append(entry_dict)

        return events

    def convertBakerKeysEvent(self, message) -> CCD_BakerKeysEvent:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BakerKeysEvent(**result)

    def convertEffectBakerAdded(self, message) -> CCD_BakerAdded:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            if type(value) == BakerKeysEvent:
                result[key] = self.convertBakerKeysEvent(value)

        return CCD_BakerAdded(**result)

    def convertBakerStakeUpdatedData(self, message) -> CCD_BakerStakeUpdatedData:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BakerStakeUpdatedData(**result)

    def convertEffectBakerStakeUpdated(self, message) -> CCD_BakerStakeUpdated:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            if type(value) == BakerStakeUpdatedData:
                result[key] = self.convertBakerStakeUpdatedData(value)

        return CCD_BakerStakeUpdated(**result)

    def convertBakerStakeIncreased(self, message) -> CCD_BakerStakeIncreased:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BakerStakeIncreased(**result)

    def convertBakerStakeDecreased(self, message) -> CCD_BakerStakeDecreased:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BakerStakeDecreased(**result)

    def convertDelegationStakeIncreased(self, message) -> CCD_DelegationStakeIncreased:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_DelegationStakeIncreased(**result)

    def convertDelegationStakeDecreased(self, message) -> CCD_DelegationStakeDecreased:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_DelegationStakeDecreased(**result)

    def convertBakerSetMetadataUrl(self, message) -> CCD_BakerSetMetadataUrl:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BakerSetMetadataUrl(**result)

    def convertDelegationSetSetRestakeEarnings(
        self, message
    ) -> CCD_DelegationSetRestakeEarnings:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_DelegationSetRestakeEarnings(**result)

    def convertBakerRestakeEarningsUpdated(
        self, message
    ) -> CCD_BakerRestakeEarningsUpdated:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BakerRestakeEarningsUpdated(**result)

    def convertDelegationSetDelegationTarget(
        self, message
    ) -> CCD_DelegationSetDelegationTarget:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) == DelegationTarget:
                result[key] = self.convertDelegationTarget(value)

        return CCD_DelegationSetDelegationTarget(**result)

    def convertBakerConfiguredEvents(self, message) -> list:
        events = []
        for entry in message:

            for descriptor in entry.DESCRIPTOR.fields:
                result = {}
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == BakerEvent.BakerStakeIncreased:
                        result[key] = self.convertBakerStakeIncreased(value)
                        events.append(result)

                    elif type(value) == BakerEvent.BakerStakeDecreased:
                        result[key] = self.convertBakerStakeDecreased(value)
                        events.append(result)

                    elif type(value) == BakerEvent.BakerSetMetadataUrl:
                        result[key] = self.convertBakerSetMetadataUrl(value)
                        events.append(result)

                    elif type(value) == BakerEvent.BakerRestakeEarningsUpdated:
                        result[key] = self.convertBakerRestakeEarningsUpdated(value)
                        events.append(result)

        return events

    def convertDelegationConfiguredEvents(self, message) -> list:
        events = []
        for entry in message:

            for descriptor in entry.DESCRIPTOR.fields:
                result = {}
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if MessageToDict(value) == {}:
                    pass
                else:
                    if type(value) == DelegationEvent.DelegationStakeIncreased:
                        result[key] = self.convertDelegationStakeIncreased(value)
                        events.append(result)

                    elif type(value) == DelegationEvent.DelegationStakeDecreased:
                        result[key] = self.convertDelegationStakeDecreased(value)
                        events.append(result)

                    elif type(value) == DelegationEvent.DelegationSetDelegationTarget:
                        result[key] = self.convertDelegationSetDelegationTarget(value)
                        events.append(result)

                    elif type(value) == DelegationEvent.DelegationSetRestakeEarnings:
                        result[key] = self.convertDelegationSetSetRestakeEarnings(value)
                        events.append(result)
        return events

    def convertEffectBakerConfigured(self, message) -> CCD_BakerConfigured:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == "events":
                result[key] = self.convertBakerConfiguredEvents(value)

        return CCD_BakerConfigured(**result)

    def convertEffectDelegationConfigured(self, message) -> CCD_DelegationConfigured:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == "events":
                result[key] = self.convertDelegationConfiguredEvents(value)

        return CCD_DelegationConfigured(**result)

    def convertEffectAccountTransfer(self, message) -> CCD_AccountTransfer:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if MessageToDict(value) == {}:
                pass
            else:
                if type(value) in self.simple_types:
                    result[key] = self.convertType(value)

        return CCD_AccountTransfer(**result)

    def convertEffectAccountTransferWithSchedule(
        self, message
    ) -> CCD_TransferredWithSchedule:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == "amount":
                result[key] = self.convertNewRelease(value)

            elif type(value) in self.simple_types:
                converted_value = self.convertType(value)
                if converted_value:
                    result[key] = converted_value

        return CCD_TransferredWithSchedule(**result)

    def convertEffectContractInitializedEvent(
        self, message
    ) -> CCD_ContractInitializedEvent:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == "events":
                result[key] = self.convertEvents(value)

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)
                # if converted_value:
                #      = converted_value

        return CCD_ContractInitializedEvent(**result)

    def convertEffectContractUpdateIssued(self, message) -> CCD_ContractUpdateIssued:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == "effects":
                result[key] = self.convertUpdateEvents(value)

        return CCD_ContractUpdateIssued(**result)

    def convertCredentialRegistrationIdEntries(self, message):
        entries = []

        for list_entry in message:
            entries.append(self.convertType(list_entry))

        return entries

    def convertCredentialsUpdated(
        self, message
    ) -> CCD_AccountTransactionEffects_CredentialsUpdated:
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if key in ["new_cred_ids", "removed_cred_ids"]:
                result[key] = self.convertCredentialRegistrationIdEntries(value)

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_AccountTransactionEffects_CredentialsUpdated(**result)

    def convertDuplicateCredIds(self, message) -> CCD_RejectReason_DuplicateCredIds:
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            result[key] = self.convertCredentialRegistrationIdEntries(value)

        return CCD_RejectReason_DuplicateCredIds(**result)

    def convertRejectReason(self, message) -> CCD_RejectReason:
        result = {}
        _type = None
        for (field, value) in message.ListFields():
            key = field.name

            # Note this next section is purely to have Coverage
            # show us that we have not covered all possible reject
            # reasons with adequate tests...
            if key == "module_not_wf":
                test_me_please = True
            if key == "module_hash_already_exists":
                test_me_please = True
            if key == "invalid_account_reference":
                test_me_please = True
            if key == "invalid_init_method":
                test_me_please = True
            if key == "invalid_receive_method":
                test_me_please = True
            if key == "invalid_module_reference":
                test_me_please = True
            if key == "invalid_contract_address":
                test_me_please = True
            if key == "runtime_failure":
                test_me_please = True
            if key == "amount_too_large":
                test_me_please = True
            if key == "serialization_failure":
                test_me_please = True
            if key == "out_of_energy":
                test_me_please = True
            if key == "rejected_init":
                test_me_please = True
            if key == "rejected_receive":
                test_me_please = True
            if key == "invalid_proof":
                test_me_please = True
            if key == "already_a_baker: ":
                test_me_please = True
            if key == "not_a_baker":
                test_me_please = True
            if key == "insufficient_balance_for_baker_stake":
                test_me_please = True
            if key == "stake_under_minimum_threshold_for_baking":
                test_me_please = True
            if key == "baker_in_cooldown":
                test_me_please = True
            if key == "duplicate_aggregation_key":
                test_me_please = True
            if key == "non_existent_credential_id":
                test_me_please = True
            if key == "key_index_already_in_use":
                test_me_please = True
            if key == "invalid_account_threshold":
                test_me_please = True
            if key == "invalid_credential_key_sign_threshold":
                test_me_please = True
            if key == "invalid_encrypted_amount_transfer_proof":
                test_me_please = True
            if key == "invalid_transfer_to_public_proof":
                test_me_please = True
            if key == "encrypted_amount_self_transfer":
                test_me_please = True
            if key == "invalid_index_on_encrypted_transfer":
                test_me_please = True
            if key == "zero_scheduledAmount":
                test_me_please = True
            if key == "non_increasing_schedule":
                test_me_please = True
            if key == "first_scheduled_release_expired":
                test_me_please = True
            if key == "scheduled_self_transfer":
                test_me_please = True
            if key == "invalid_credentials":
                test_me_please = True
            if key == "duplicate_cred_ids":
                test_me_please = True
            if key == "non_existent_cred_ids":
                test_me_please = True
            if key == "remove_first_credential":
                test_me_please = True
            if key == "credential_holder_did_not_sign":
                test_me_please = True
            if key == "not_allowed_multiple_credentials":
                test_me_please = True
            if key == "not_allowed_to_receive_encrypted":
                test_me_please = True
            if key == "not_allowed_to_handle_encrypted":
                test_me_please = True
            if key == "missing_baker_add_parameters":
                test_me_please = True
            if key == "finalization_reward_commission_not_in_range":
                test_me_please = True
            if key == "baking_reward_commission_not_in_range":
                test_me_please = True
            if key == "transaction_fee_commission_not_in_range":
                test_me_please = True
            if key == "already_a_delegator":
                test_me_please = True
            if key == "insufficient_balance_for_delegation_stake":
                test_me_please = True
            if key == "missing_delegation_add_parameters":
                test_me_please = True
            if key == "insufficient_delegation_stak":
                test_me_please = True
            if key == "delegator_in_cooldown":
                test_me_please = True
            if key == "not_a_delegator":
                test_me_please = True
            if key == "delegation_target_not_a_baker: ":
                test_me_please = True
            if key == "stake_over_maximum_threshold_for_pool":
                test_me_please = True
            if key == "pool_would_become_over_delegated":
                test_me_please = True
            if key == "pool_closed":
                test_me_please = True

            _type = key
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) in [
                RejectReason.InvalidInitMethod,
                RejectReason.InvalidReceiveMethod,
                RejectReason.AmountTooLarge,
                RejectReason.RejectedInit,
                RejectReason.RejectedReceive,
            ]:
                result[key] = self.convertTypeWithSingleValues(value)

            elif type(value) == RejectReason.DuplicateCredIds:
                result[key] = self.convertDuplicateCredIds(value)
        return result, _type

    def convertRejectReasonNone(self, message) -> CCD_AccountTransactionEffects_None:
        result = {}
        _type = None
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) == RejectReason:
                result[key], _type = self.convertRejectReason(value)

        return CCD_AccountTransactionEffects_None(**result), _type

    def convertEffectAccountEncryptedAmountTransferred(
        self, message
    ) -> CCD_AccountTransactionEffects_EncryptedAmountTransferred:
        result = {}
        _type = None
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) in [EncryptedAmountRemovedEvent, NewEncryptedAmountEvent]:
                result[key] = self.convertTypeWithSingleValues(value)

        return CCD_AccountTransactionEffects_EncryptedAmountTransferred(**result)

    def convertEffectAccountTransferredToPublic(
        self, message
    ) -> CCD_AccountTransactionEffects_TransferredToPublic:
        result = {}
        _type = None
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) in [EncryptedAmountRemovedEvent]:
                result[key] = self.convertTypeWithSingleValues(value)

        return CCD_AccountTransactionEffects_TransferredToPublic(**result)

    def convertAccountTransactionEffects(
        self, message
    ) -> CCD_AccountTransactionEffects:
        result = {}
        _type = {"type": "account_transaction"}
        for (field, value) in message.ListFields():
            key = field.name
            _outcome = "success"
            try:
                if value.HasField("reject_reason"):
                    _outcome = "reject"
                    result[key], type_contents = self.convertRejectReasonNone(value)
                    _type.update({"contents": type_contents})
            except:

                if _outcome == "success":

                    if type(value) == ContractInitializedEvent:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectContractInitializedEvent(value)

                    elif type(value) == AccountTransactionEffects.ContractUpdateIssued:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectContractUpdateIssued(value)

                    elif type(value) == AccountTransactionEffects.AccountTransfer:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectAccountTransfer(value)

                    elif type(value) == BakerEvent.BakerAdded:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectBakerAdded(value)

                    elif type(value) == BakerId:
                        _type.update({"contents": key})
                        result[key] = self.convertType(value)

                    elif type(value) == AccountTransactionEffects.BakerStakeUpdated:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectBakerStakeUpdated(value)

                    elif type(value) == BakerEvent.BakerRestakeEarningsUpdated:
                        _type.update({"contents": key})
                        result[key] = self.convertTypeWithSingleValues(value)

                    elif type(value) == BakerKeysEvent:
                        _type.update({"contents": key})
                        result[key] = self.convertBakerKeysEvent(value)

                    elif (
                        type(value)
                        == AccountTransactionEffects.EncryptedAmountTransferred
                    ):
                        _type.update({"contents": key})
                        result[
                            key
                        ] = self.convertEffectAccountEncryptedAmountTransferred(value)

                    elif type(value) == EncryptedSelfAmountAddedEvent:
                        _type.update({"contents": key})
                        result[key] = CCD_EncryptedSelfAmountAddedEvent(
                            **self.convertTypeWithSingleValues(value)
                        )

                    elif type(value) == AccountTransactionEffects.TransferredToPublic:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectAccountTransferredToPublic(
                            value
                        )

                    elif (
                        type(value) == AccountTransactionEffects.TransferredWithSchedule
                    ):
                        _type.update({"contents": key})
                        result[key] = self.convertEffectAccountTransferWithSchedule(
                            value
                        )

                    elif type(value) == AccountTransactionEffects.CredentialsUpdated:
                        _type.update({"contents": key})
                        result[key] = self.convertCredentialsUpdated(value)

                    elif type(value) == RegisteredData:
                        _type.update({"contents": key})
                        result[key] = self.convertType(value)

                    elif type(value) == AccountTransactionEffects.BakerConfigured:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectBakerConfigured(value)

                    elif type(value) == AccountTransactionEffects.DelegationConfigured:
                        _type.update({"contents": key})
                        result[key] = self.convertEffectDelegationConfigured(value)

                    elif type(value) in self.simple_types:
                        _type.update({"contents": key})
                        result[key] = self.convertType(value)

        return CCD_AccountTransactionEffects(**result), _type, _outcome

    def convertAccountTransactionDetails(
        self, message
    ) -> CCD_AccountTransactionDetails:
        result = {}
        for (field, value) in message.ListFields():
            key = field.name
            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            if type(value) == AccountTransactionEffects:
                (
                    result[key],
                    _type,
                    result["outcome"],
                ) = self.convertAccountTransactionEffects(value)

        return CCD_AccountTransactionDetails(**result), CCD_TransactionType(**_type)

    def convertAccountCreationDetails(self, message) -> CCD_AccountCreationDetails:
        result = {}
        _type = {"type": "account_creation"}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if key == "credential_type":
                result[key] = value
                _type.update({"contents": CCD_CredentialType(value).name})

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_AccountCreationDetails(**result), CCD_TransactionType(**_type)

    def convertUpdatePayload(self, message) -> CCD_UpdatePayload:
        result = {}
        _type = {"type": "update"}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if self.valueIsEmpty(value):
                pass
            else:
                _type.update({"contents": key})

                if type(value) == ExchangeRate:
                    value_as_dict = MessageToDict(value)
                    result[key] = CCD_ExchangeRate(
                        **{
                            "numerator": value_as_dict["value"]["numerator"],
                            "denominator": value_as_dict["value"]["denominator"],
                        }
                    )

                elif type(value) in [BakerStakeThreshold, ProtocolUpdate]:
                    result[key] = self.convertTypeWithSingleValues(value)

                elif type(value) == Level1Update:
                    result[key] = self.convertLevel1Update(value)

                elif type(value) == IpInfo:
                    result[key] = self.convertIpInfo(value)

                # TODO: no test available
                elif type(value) == ElectionDifficulty:
                    result[key] = self.convertElectionDifficulty(value)

                # TODO: no test available
                elif type(value) == MintDistributionCpv0:
                    result[key] = self.convertMintDistributionCpv0(value)

                # TODO: no test available
                elif type(value) == TransactionFeeDistribution:
                    result[key] = self.convertTransactionFeeDistribution(value)

                # TODO: no test available
                elif type(value) == GasRewards:
                    result[key] = self.convertGasRewards(value)

                # TODO: no test available
                elif type(value) == RootUpdate:
                    result[key] = self.convertRootUpdate(value)

                # TODO: no test available
                elif type(value) == ArInfo:
                    result[key] = self.convertArInfo(value)

                # TODO: no test available
                elif type(value) == CooldownParametersCpv1:
                    result[key] = self.convertCooldownParametersCpv1(value)

                # TODO: no test available
                elif type(value) == PoolParametersCpv1:
                    result[key] = self.convertPoolParametersCpv1(value)

                # TODO: no test available
                elif type(value) == TimeParametersCpv1:
                    result[key] = self.convertTimeParametersCpv1(value)

                # TODO: no test available
                elif type(value) == MintDistributionCpv1:
                    result[key] = self.convertMintDistributionCpv1(value)

                elif type(value) in self.simple_types:
                    result[key] = self.convertType(value)

        return CCD_UpdatePayload(**result), _type

    def convertUpdateDetails(self, message) -> CCD_UpdateDetails:
        result = {}
        _type = {"type": "update"}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if self.valueIsEmpty(value):
                pass
            else:
                if type(value) == UpdatePayload:
                    result[key], _type = self.convertUpdatePayload(value)

                elif type(value) in self.simple_types:
                    result[key] = self.convertType(value)

        return CCD_UpdateDetails(**result), CCD_TransactionType(**_type)

    def get_block_transaction_events(self: GRPCClient, block_hash: str) -> CCD_Block:
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value = self.stub.GetBlockTransactionEvents(request=blockHashInput)

        tx_list = []
        for tx in list(grpc_return_value):
            result = {}
            for (field, value) in tx.ListFields():
                key = field.name
                if type(value) in self.simple_types:
                    result[key] = self.convertType(value)

                if type(value) == UpdateDetails:
                    result[key], result["type"] = self.convertUpdateDetails(value)

                if type(value) == AccountCreationDetails:
                    result[key], result["type"] = self.convertAccountCreationDetails(
                        value
                    )

                if type(value) == AccountTransactionDetails:
                    result[key], result["type"] = self.convertAccountTransactionDetails(
                        value
                    )

            tx_list.append(CCD_BlockItemSummary(**result))

        return CCD_Block(**{"transaction_summaries": tx_list})
