from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.messages.responses.IResponse import IResponse, IResponseGetterMixin
from iqrfpy.messages.requests.coordinator.SetDpaParams import DpaParam
from iqrfpy.enums.Commands import CoordinatorResponseCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common

__all__ = ['SetDpaParamsResponse']


@typechecked
class SetDpaParamsResponse(IResponseGetterMixin):
    __slots__ = '_dpa_param'

    def __init__(self, hwpid: int = Common.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.SET_DPA_PARAMS,
            m_type=CoordinatorMessages.SET_DPA_PARAMS,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == 0:
            self._dpa_param: DpaParam = DpaParam(result['prevDpaParam'])

    def get_dpa_param(self) -> DpaParam:
        return self._dpa_param

    @staticmethod
    def from_dpa(dpa: bytes) -> SetDpaParamsResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[5], dpa[4])
        rcode = dpa[6]
        result = None
        if rcode == 0:
            if len(dpa) != 9:
                raise ValueError('Invalid dpa length')
            result = {'prevDpaParam': dpa[8]}
        return SetDpaParamsResponse(hwpid=hwpid, rcode=dpa[6], dpa_value=dpa[7], result=result)

    @staticmethod
    def from_json(json: dict) -> SetDpaParamsResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == 0 else None
        return SetDpaParamsResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
