from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.messages.responses.IResponse import IResponse, IResponseGetterMixin
from iqrfpy.enums.Commands import CoordinatorResponseCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common

__all__ = ['ClearAllBondsResponse']


@typechecked
class ClearAllBondsResponse(IResponseGetterMixin):

    def __init__(self, hwpid: int = Common.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.CLEAR_ALL_BONDS,
            m_type=CoordinatorMessages.CLEAR_ALL_BONDS,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )

    @staticmethod
    def from_dpa(dpa: bytes) -> ClearAllBondsResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[5], dpa[4])
        if len(dpa) != 8:
            raise ValueError('Invalid dpa length')
        return ClearAllBondsResponse(hwpid=hwpid, rcode=dpa[6], dpa_value=dpa[7], result=None)

    @staticmethod
    def from_json(json: dict) -> ClearAllBondsResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == 0 else None
        return ClearAllBondsResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
