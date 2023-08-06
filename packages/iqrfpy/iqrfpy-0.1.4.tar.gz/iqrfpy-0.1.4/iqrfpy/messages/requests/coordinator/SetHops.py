from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['SetHopsRequest']


@typechecked
class SetHopsRequest(IRequest):
    __slots__ = '_request_hops', '_response_hops'

    def __init__(self, request_hops: int, response_hops: int, hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_HOPS,
            m_type=CoordinatorMessages.SET_HOPS,
            hwpid=hwpid,
            msgid=msgid
        )
        self._request_hops = request_hops
        self._response_hops = response_hops
        self._validate()

    def _validate(self) -> None:
        if (self._request_hops < 0 or self._request_hops > 239) and self._request_hops != 255:
            raise ValueError('Request hops value should be between 0 and 239, or 255.')
        if (self._response_hops < 1 or self._response_hops > 239) and self._response_hops != 255:
            raise ValueError('Response hops value should be between 1 and 239, or 255.')

    def set_request_hops(self, request_hops: int) -> None:
        self._request_hops = request_hops

    def set_response_hops(self, response_hops: int) -> None:
        self._response_hops = response_hops

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._request_hops, self._response_hops]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'requestHops': self._request_hops, 'responseHops': self._response_hops}
        return super().to_json()
