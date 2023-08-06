from __future__ import annotations
from typing import Optional
from iqrfpy.enums.Commands import Command
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.utils.common import Common
from iqrfpy.messages.responses.IResponse import IResponseGetterMixin

__all__ = ['Confirmation']


class Confirmation(IResponseGetterMixin):
    __slots__ = '_request_hops', '_response_hops', '_timeslot'

    def __init__(self, nadr: int, pnum: Peripheral, pcmd: Command, hwpid: int, dpa_value: int, rcode: int,
                 result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pcmd=pcmd,
            pnum=pnum,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            result=result
        )
        self._request_hops: int = result['requestHops']
        self._response_hops: int = result['responseHops']
        self._timeslot: int = result['timeslot']

    def get_request_hops(self) -> int:
        return self._request_hops

    def get_response_hops(self) -> int:
        return self._response_hops

    def get_timeslot(self) -> int:
        return self._timeslot

    @staticmethod
    def from_dpa(dpa: bytes) -> Confirmation:
        if len(dpa) != 11:
            raise ValueError('Invalid DPA confirmation packet length.')
        if dpa[6] != 0xFF:
            raise ValueError('Not a DPA confirmation packet.')
        pnum = Common.pnum_from_dpa(dpa[2])
        pcmd = Common.request_pcmd_from_dpa(pnum, dpa[3])
        hwpid = Common.hwpid_from_dpa(dpa[5], dpa[4])
        result = {'requestHops': dpa[8], 'responseHops': dpa[10], 'timeslot': dpa[9]}
        return Confirmation(nadr=dpa[0], pnum=pnum, pcmd=pcmd, hwpid=hwpid, rcode=dpa[6], dpa_value=dpa[7],
                            result=result)

    @staticmethod
    def from_json(json: dict) -> Confirmation:
        raise NotImplementedError('from_json() method not implemented.')
