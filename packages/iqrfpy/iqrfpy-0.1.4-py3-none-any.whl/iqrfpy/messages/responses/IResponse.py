from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from iqrfpy.enums.Commands import Command, CoordinatorResponseCommands
from iqrfpy.enums.MessageTypes import MessageType
from iqrfpy.enums.peripherals import Peripheral, EmbedPeripherals
from iqrfpy.utils.common import Common

__all__ = ['IResponse', 'IResponseGetterMixin']


class IResponse(ABC):

    ASYNC_MSGID = 'async'

    def __init__(self, nadr: int, pnum: Peripheral, pcmd: Command, hwpid: int = Common.HWPID_MAX, rcode: int = 0,
                 dpa_value: int = 0, pdata: Optional[bytes] = None, m_type: Optional[MessageType] = None,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        self._nadr: int = nadr
        self._pnum: Peripheral = pnum
        self._pcmd: Command = pcmd
        self._mtype = m_type
        self._hwpid: int = hwpid
        self._rcode = rcode
        self._dpa_value: int = dpa_value
        self._pdata = pdata
        self._msgid = msgid
        self._result = result

    @abstractmethod
    def get_nadr(self) -> int:
        return self._nadr

    @abstractmethod
    def get_pnum(self) -> Peripheral:
        return self._pnum

    @abstractmethod
    def get_pcmd(self) -> Command:
        return self._pcmd

    @abstractmethod
    def get_mtype(self) -> MessageType:
        return self._mtype

    @abstractmethod
    def get_hwpid(self) -> int:
        return self._hwpid

    @abstractmethod
    def get_rcode(self) -> int:
        return self._rcode

    @abstractmethod
    def get_dpa_value(self) -> int:
        return self._dpa_value

    @abstractmethod
    def get_pdata(self) -> bytes:
        return self._pdata

    @abstractmethod
    def get_result(self) -> dict:
        return self._result

    @abstractmethod
    def get_msgid(self) -> str:
        return self._msgid

    @staticmethod
    def validate_dpa_response(data: bytes) -> None:
        if len(data) < 8:
            raise ValueError('Response packet too short.')

    @staticmethod
    @abstractmethod
    def from_dpa(dpa: bytes) -> IResponse:
        IResponse.validate_dpa_response(data)
        pnum = data[2]
        pcmd = data[3]
        rcode = data[6]
        if rcode == 0xFF and len(data) == 11:
            from iqrfpy.messages.responses.Confirmation import Confirmation
            return Confirmation.from_dpa(data)
        if pcmd <= 127 and rcode >= 128:
            from iqrfpy.messages.responses.AsyncResponse import AsyncResponse
            return AsyncResponse.from_dpa(data)
        match pnum:
            case EmbedPeripherals.COORDINATOR:
                match pcmd:
                    case CoordinatorResponseCommands.ADDR_INFO:
                        from iqrfpy.messages.responses.coordinator import AddrInfoResponse
                        return AddrInfoResponse.from_dpa(data)
                    case CoordinatorResponseCommands.BACKUP:
                        from iqrfpy.messages.responses.coordinator import BackupResponse
                        return BackupResponse.from_dpa(data)
                    case CoordinatorResponseCommands.BONDED_DEVICES:
                        from iqrfpy.messages.responses.coordinator import BondedDevicesResponse
                        return BondedDevicesResponse.from_dpa(data)
                    case CoordinatorResponseCommands.BOND_NODE:
                        from iqrfpy.messages.responses.coordinator import BondNodeResponse
                        return BondNodeResponse.from_dpa(data)
                    case CoordinatorResponseCommands.CLEAR_ALL_BONDS:
                        from iqrfpy.messages.responses.coordinator import ClearAllBondsResponse
                        return ClearAllBondsResponse.from_dpa(data)
                    case CoordinatorResponseCommands.DISCOVERED_DEVICES:
                        from iqrfpy.messages.responses.coordinator import DiscoveredDevicesResponse
                        return DiscoveredDevicesResponse.from_dpa(data)
                    case CoordinatorResponseCommands.DISCOVERY:
                        from iqrfpy.messages.responses.coordinator import DiscoveryResponse
                        return DiscoveryResponse.from_dpa(data)
                    case CoordinatorResponseCommands.REMOVE_BOND:
                        from iqrfpy.messages.responses.coordinator import RemoveBondResponse
                        return RemoveBondResponse.from_dpa(data)
                    case CoordinatorResponseCommands.RESTORE:
                        from iqrfpy.messages.responses.coordinator import RestoreResponse
                        return RestoreResponse.from_dpa(data)
                    case CoordinatorResponseCommands.SET_DPA_PARAMS:
                        from iqrfpy.messages.responses.coordinator import SetDpaParamsResponse
                        return SetDpaParamsResponse.from_dpa(data)
                    case CoordinatorResponseCommands.SET_HOPS:
                        from iqrfpy.messages.responses.coordinator import SetHopsResponse
                        return SetHopsResponse.from_dpa(data)
                    case CoordinatorResponseCommands.SET_MID:
                        from iqrfpy.messages.responses.coordinator import SetMIDResponse
                        return SetMIDResponse.from_dpa(data)
                    case CoordinatorResponseCommands.SMART_CONNECT:
                        from iqrfpy.messages.responses.coordinator import SmartConnectResponse
                        return SmartConnectResponse.from_dpa(data)
                    case _:
                        raise ValueError(f'Unknown or unsupported peripheral command: {pcmd}')
            case _:
                raise ValueError(f'Unknown or unsupported peripheral: {pnum}')

    @staticmethod
    @abstractmethod
    def from_json(json: dict) -> IResponse:
        pass


class IResponseGetterMixin(IResponse):

    def get_nadr(self) -> int:
        return super().get_nadr()

    def get_pnum(self) -> Peripheral:
        return super().get_pnum()

    def get_pcmd(self) -> Command:
        return super().get_pcmd()

    def get_mtype(self) -> MessageType:
        return super().get_mtype()

    def get_hwpid(self) -> int:
        return super().get_hwpid()

    def get_rcode(self) -> int:
        return super().get_rcode()

    def get_dpa_value(self) -> int:
        return super().get_dpa_value()

    def get_pdata(self) -> bytes:
        return super().get_pdata()

    def get_result(self) -> dict:
        return super().get_result()

    def get_msgid(self) -> str:
        return super().get_msgid()

    @staticmethod
    def from_dpa(dpa: bytes) -> IResponse:
        raise NotImplementedError('from_dpa() method not implemented.')

    @staticmethod
    def from_json(json: dict) -> IResponse:
        raise NotImplementedError('from_json() method not implemented.')
