from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import List, Union
from iqrfpy.enums.Commands import CoordinatorRequestCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['RestoreRequest']


@typechecked
class RestoreRequest(IRequest):
    __slots__ = '_network_data'

    def __init__(self, network_data: List[int], hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.RESTORE,
            m_type=CoordinatorMessages.RESTORE,
            hwpid=hwpid,
            msgid=msgid
        )
        self._network_data = network_data
        self._validate()

    def _validate(self) -> None:
        if not Common.values_in_byte_range(self._network_data):
            raise ValueError('Network data block values should be between 0 and 255.')
        if len(self._network_data) != 49:
            raise ValueError('Network data should be 49 blocks long.')

    def set_network_data(self, network_data: List[int]) -> None:
        self._network_data = network_data

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate()
        self._pdata = self._network_data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._validate()
        self._params = {'networkData': self._network_data}
        return super().to_json()
