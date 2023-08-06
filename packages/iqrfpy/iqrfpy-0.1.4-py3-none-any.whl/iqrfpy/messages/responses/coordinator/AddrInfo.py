from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.messages.responses.IResponse import IResponse, IResponseGetterMixin
from iqrfpy.enums.Commands import CoordinatorResponseCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common

__all__ = ['AddrInfoResponse']


@typechecked
class AddrInfoResponse(IResponseGetterMixin):
    __slots__ = '_dev_nr', '_did'

    def __init__(self, hwpid: int = 0xFFFF, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.ADDR_INFO,
            m_type=CoordinatorMessages.ADDR_INFO,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == 0:
            self._dev_nr = result['devNr']
            self._did = result['did']

    def get_dev_nr(self) -> int:
        return self._dev_nr

    def get_did(self) -> int:
        return self._did

    @staticmethod
    def from_dpa(dpa: bytes) -> AddrInfoResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[5], dpa[4])
        rcode = dpa[6]
        result = None
        if rcode == 0:
            if len(dpa) != 10:
                raise ValueError('Invalid dpa length')
            result = {'devNr': dpa[8], 'did': dpa[9]}
        return AddrInfoResponse(hwpid=hwpid, rcode=rcode, dpa_value=dpa[7], result=result)

    @staticmethod
    def from_json(json: dict) -> AddrInfoResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == 0 else None
        return AddrInfoResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
