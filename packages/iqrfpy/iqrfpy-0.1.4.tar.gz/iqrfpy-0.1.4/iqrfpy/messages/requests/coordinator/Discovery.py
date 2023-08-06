from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['DiscoveryRequest']


@typechecked
class DiscoveryRequest(IRequest):
    __slots__ = '_tx_power', '_max_addr'

    def __init__(self, tx_power: int, max_addr: int, hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())) -> None:
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.DISCOVERY,
            m_type=CoordinatorMessages.DISCOVERY,
            hwpid=hwpid,
            msgid=msgid
        )
        self._tx_power = tx_power
        self._max_addr = max_addr
        self._validate()

    def _validate(self) -> None:
        if self._tx_power < 0 or self._tx_power > 7:
            raise ValueError('TX power value should be between 0 and 7.')
        if self._max_addr < 0 or self._max_addr > 239:
            raise ValueError('Max address value should be between 0 and 239.')

    def set_tx_power(self, tx_power: int) -> None:
        self._tx_power = tx_power

    def set_max_addr(self, max_addr: int) -> None:
        self._max_addr = max_addr

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._tx_power, self._max_addr]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'txPower': self._tx_power, 'maxAddr': self._max_addr}
        return super().to_json()
