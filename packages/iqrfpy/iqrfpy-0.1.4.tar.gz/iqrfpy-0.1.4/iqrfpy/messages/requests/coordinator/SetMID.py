from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['SetMIDRequest']


@typechecked
class SetMIDRequest(IRequest):
    __slots__ = '_bond_addr', '_mid'

    def __init__(self, bond_addr: int, mid: int, hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_MID,
            m_type=CoordinatorMessages.SET_MID,
            hwpid=hwpid,
            msgid=msgid
        )
        self._bond_addr = bond_addr
        self._mid = mid
        self._validate()

    def _validate(self) -> None:
        if self._bond_addr < 1 or self._bond_addr > 239:
            raise ValueError('Bond address value should be between 1 and 239.')
        if self._mid < 0 or self._mid > 0xFFFFFFFF:
            raise ValueError('MID value should be an unsigned 32bit integer.')

    def set_bond_addr(self, bond_addr: int) -> None:
        self._bond_addr = bond_addr

    def set_mid(self, mid: int) -> None:
        self._mid = mid

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [
            self._mid & 0xFF,
            (self._mid >> 8) & 0xFF,
            (self._mid >> 16) & 0xFF,
            (self._mid >> 24) & 0xFF,
            self._bond_addr
        ]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'bondAddr': self._bond_addr, 'mid': self._mid}
        return super().to_json()
