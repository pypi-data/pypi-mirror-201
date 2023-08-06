from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['BackupRequest']


@typechecked
class BackupRequest(IRequest):
    __slots__ = '_index'

    def __init__(self, index: int = 0, hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.BACKUP,
            m_type=CoordinatorMessages.BACKUP,
            hwpid=hwpid,
            msgid=msgid
        )
        self._index = index
        self._validate()

    def _validate(self) -> None:
        if self._index < 0 or self._index > 255:
            raise ValueError('Index value should be between 0 and 255.')

    def set_index(self, index: int) -> None:
        self._index = index

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = [self._index]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'index': self._index}
        return super().to_json()
