from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['RemoveBondRequest']


@typechecked
class RemoveBondRequest(IRequest):
    __slots__ = '_bond_addr'

    def __init__(self, bond_addr: int, hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.REMOVE_BOND,
            m_type=CoordinatorMessages.REMOVE_BOND,
            hwpid=hwpid,
            msgid=msgid
        )
        self._bond_addr = bond_addr
        self._validate()

    def _validate(self) -> None:
        if self._bond_addr < 1 or self._bond_addr > 239:
            raise ValueError('Bond address value should be between 1 and 239.')

    def set_bond_addr(self, bond_addr: int) -> None:
        self._bond_addr = bond_addr

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._bond_addr]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'bondAddr': self._bond_addr}
        return super().to_json()
