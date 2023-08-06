from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import Union
from iqrfpy.enums.Commands import NodeRequestCommands
from iqrfpy.enums.MessageTypes import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.requests.IRequest import IRequest

__all__ = ['ReadRequest']


@typechecked
class ReadRequest(IRequest):

    def __init__(self, nadr: int, hwpid: int = Common.HWPID_MAX, msgid: str = str(uuid4())):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.READ,
            m_type=NodeMessages.READ,
            hwpid=hwpid,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        return super().to_json()
