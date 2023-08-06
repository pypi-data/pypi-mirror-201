from __future__ import annotations
from typeguard import typechecked
from typing import Optional
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.enums.Commands import Command
from iqrfpy.enums.MessageTypes import GenericMessages
from .IResponse import IResponse, IResponseGetterMixin
from iqrfpy.utils.common import Common

__all__ = ['AsyncResponse']


@typechecked
class AsyncResponse(IResponseGetterMixin):

    def __init__(self, nadr: int, pnum: Peripheral, pcmd: Command, hwpid: int = Common.HWPID_MAX, rcode: int = 0x80,
                 dpa_value: int = 0, pdata: Optional[bytes] = None, msgid: Optional[str] = None,
                 result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=pnum,
            pcmd=pcmd,
            m_type=GenericMessages.RAW,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            pdata=pdata,
            msgid=msgid,
            result=result
        )

    @staticmethod
    def from_dpa(dpa: bytes) -> AsyncResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[5], dpa[4])
        pnum = Common.pnum_from_dpa(dpa[2])
        pcmd = Common.request_pcmd_from_dpa(pnum, dpa[3])
        rcode = dpa[6]
        result = None
        if rcode == 0x80:
            if len(dpa) > 8:
                result = {'rData': list(dpa)}
        return AsyncResponse(nadr=dpa[0], pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=rcode,
                             dpa_value=dpa[7], pdata=dpa, result=result)

    @staticmethod
    def from_json(json: dict) -> AsyncResponse:
        msgid = Common.msgid_from_json(json)
        result = json['data']['rsp']
        packet = result['rData'].replace('.', '')
        pdata = bytes.fromhex(packet)
        ldata = Common.hex_string_to_list(packet)
        hwpid = Common.hwpid_from_dpa(ldata[5], ldata[4])
        pnum = Common.pnum_from_dpa(ldata[2])
        pcmd = Common.request_pcmd_from_dpa(pnum, ldata[3])
        return AsyncResponse(nadr=ldata[0], pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=ldata[6],
                             dpa_value=ldata[7], pdata=pdata, msgid=msgid, result=result)
