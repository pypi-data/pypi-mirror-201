from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['BondNodeRequest']


@typechecked
class BondNodeRequest(IRequest):
    __slots__ = '_req_addr', '_bonding_test_retries'

    def __init__(self, req_addr: int, bonding_test_retries: int, hwpid: int = Common.HWPID_MAX,
                 msgid: str = str(uuid4())) -> None:
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.BOND_NODE,
            m_type=CoordinatorMessages.BOND_NODE,
            hwpid=hwpid,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries
        self._validate()

    def _validate(self) -> None:
        if self._req_addr == 240 and self._bonding_test_retries == 0:
            return
        if self._req_addr < 0 or self._req_addr > 239:
            raise ValueError('Address value should be between 0 and 239. Value 240 is allowed in combination with \
            bonding test retries value 0.')
        if self._bonding_test_retries < 0 or self._bonding_test_retries > 255:
            raise ValueError('Bonding test retries value should be between 0 and 255.')

    def set_req_addr(self, req_addr: int) -> None:
        self._req_addr = req_addr

    def set_bonding_test_retries(self, bonding_test_retries: int) -> None:
        self._bonding_test_retries = bonding_test_retries

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._req_addr, self._bonding_test_retries]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'reqAddr': self._req_addr, 'bondingMask': self._bonding_test_retries}
        return super().to_json()
