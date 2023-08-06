from abc import ABC, abstractmethod
from ..enums.MessageTypes import *
from .responses.AsyncResponse import AsyncResponse
from .responses.Confirmation import Confirmation
from .responses.IResponse import IResponse
from .responses.coordinator import *
from ..utils.common import Common

__all__ = [
    'ResponseFactory',
    '_get_factory_from_mtype',
    'AsyncResponseFactory',
    'ConfirmationFactory',
    'CoordinatorAddrInfoFactory',
    'CoordinatorAuthorizeBondFactory',
    'CoordinatorBackupFactory',
    'CoordinatorBondedDevicesFactory',
    'CoordinatorBondNodeFactory',
    'CoordinatorClearAllBondsFactory',
    'CoordinatorDiscoveredDevicesFactory',
    'CoordinatorDiscoveryFactory',
    'CoordinatorRemoveBondFactory',
    'CoordinatorRestoreFactory',
    'CoordinatorSetDpaParamsFactory',
    'CoordinatorSetHopsFactory',
    'CoordinatorSetMIDFactory',
    'CoordinatorSmartConnectFactory'
]


class ResponseFactory:

    @staticmethod
    def get_response_from_dpa(dpa: bytes) -> IResponse:
        IResponse.validate_dpa_response(dpa)
        pnum = dpa[2]
        pcmd = dpa[3]
        rcode = dpa[6]
        if rcode == 0xFF and len(dpa) == 11:
            factory = ConfirmationFactory()
        elif pcmd <= 127 and rcode >= 128:
            factory = AsyncResponseFactory()
        else:
            mtype = Common.mtype_from_dpa_response(pnum, pcmd)
            factory = _get_factory_from_mtype(mtype)
        return factory.create_from_dpa(dpa)

    @staticmethod
    def get_response_from_json(json: dict) -> IResponse:
        msgid = Common.msgid_from_json(json)
        mtype = Common.mtype_str_from_json(json)
        if msgid == IResponse.ASYNC_MSGID and \
                GenericMessages.has_value(mtype) and GenericMessages(mtype) == GenericMessages.RAW:
            factory = AsyncResponseFactory()
        else:
            message = Common.string_to_mtype(mtype)
            factory = _get_factory_from_mtype(message)
        return factory.create_from_json(json)


class BaseFactory(ABC):

    @abstractmethod
    def create_from_dpa(self, dpa: bytes) -> IResponse:
        """Returns a response object created from DPA message."""

    @abstractmethod
    def create_from_json(self, json: dict) -> IResponse:
        """Returns a response object created from JSON API message."""


class ConfirmationFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> Confirmation:
        return Confirmation.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> Confirmation:
        return Confirmation.from_json(json=json)


class AsyncResponseFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> IResponse:
        return AsyncResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> IResponse:
        return AsyncResponse.from_json(json=json)


class CoordinatorAddrInfoFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> AddrInfoResponse:
        return AddrInfoResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> AddrInfoResponse:
        return AddrInfoResponse.from_json(json=json)


class CoordinatorAuthorizeBondFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> AuthorizeBondResponse:
        return AuthorizeBondResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> AuthorizeBondResponse:
        return AuthorizeBondResponse.from_json(json=json)


class CoordinatorBackupFactory(BaseFactory):

    def create_from_dpa(self, dpa: bytes) -> BackupResponse:
        return BackupResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> BackupResponse:
        return BackupResponse.from_json(json=json)


class CoordinatorBondedDevicesFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> BondedDevicesResponse:
        return BondedDevicesResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> BondedDevicesResponse:
        return BondedDevicesResponse.from_json(json=json)


class CoordinatorBondNodeFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> BondNodeResponse:
        return BondNodeResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> BondNodeResponse:
        return BondNodeResponse.from_json(json=json)


class CoordinatorClearAllBondsFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> ClearAllBondsResponse:
        return ClearAllBondsResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> ClearAllBondsResponse:
        return ClearAllBondsResponse.from_json(json=json)


class CoordinatorDiscoveredDevicesFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> DiscoveredDevicesResponse:
        return DiscoveredDevicesResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> DiscoveredDevicesResponse:
        return DiscoveredDevicesResponse.from_json(json=json)


class CoordinatorDiscoveryFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> DiscoveryResponse:
        return DiscoveryResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> DiscoveryResponse:
        return DiscoveryResponse.from_json(json=json)


class CoordinatorRemoveBondFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> RemoveBondResponse:
        return RemoveBondResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> RemoveBondResponse:
        return RemoveBondResponse.from_json(json=json)


class CoordinatorRestoreFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> RestoreResponse:
        return RestoreResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> RestoreResponse:
        return RestoreResponse.from_json(json=json)


class CoordinatorSetDpaParamsFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SetDpaParamsResponse:
        return SetDpaParamsResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SetDpaParamsResponse:
        return SetDpaParamsResponse.from_json(json=json)


class CoordinatorSetHopsFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SetHopsResponse:
        return SetHopsResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SetHopsResponse:
        return SetHopsResponse.from_json(json=json)


class CoordinatorSetMIDFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SetMIDResponse:
        return SetMIDResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SetMIDResponse:
        return SetMIDResponse.from_json(json=json)


class CoordinatorSmartConnectFactory(BaseFactory):
    def create_from_dpa(self, dpa: bytes) -> SmartConnectResponse:
        return SmartConnectResponse.from_dpa(dpa=dpa)

    def create_from_json(self, json: dict) -> SmartConnectResponse:
        return SmartConnectResponse.from_json(json=json)


def _get_factory_from_mtype(mtype: MessageType) -> BaseFactory:
    factories = {
        CoordinatorMessages.ADDR_INFO: CoordinatorAddrInfoFactory(),
        CoordinatorMessages.AUTHORIZE_BOND: CoordinatorAuthorizeBondFactory(),
        CoordinatorMessages.BACKUP: CoordinatorBackupFactory(),
        CoordinatorMessages.BONDED_DEVICES: CoordinatorBondedDevicesFactory(),
        CoordinatorMessages.BOND_NODE: CoordinatorBondNodeFactory(),
        CoordinatorMessages.CLEAR_ALL_BONDS: CoordinatorClearAllBondsFactory(),
        CoordinatorMessages.DISCOVERED_DEVICES: CoordinatorDiscoveredDevicesFactory(),
        CoordinatorMessages.DISCOVERY: CoordinatorDiscoveryFactory(),
        CoordinatorMessages.REMOVE_BOND: CoordinatorRemoveBondFactory(),
        CoordinatorMessages.RESTORE: CoordinatorRestoreFactory(),
        CoordinatorMessages.SET_DPA_PARAMS: CoordinatorSetDpaParamsFactory(),
        CoordinatorMessages.SET_HOPS: CoordinatorSetHopsFactory(),
        CoordinatorMessages.SET_MID: CoordinatorSetMIDFactory(),
        CoordinatorMessages.SMART_CONNECT: CoordinatorSmartConnectFactory(),
    }

    if mtype in factories:
        return factories[mtype]
    raise ValueError(f'Unknown or unsupported message type: {mtype}')
