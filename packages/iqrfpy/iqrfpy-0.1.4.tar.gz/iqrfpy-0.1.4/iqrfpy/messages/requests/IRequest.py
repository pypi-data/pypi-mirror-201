from __future__ import annotations
from typeguard import typechecked
from abc import ABC, abstractmethod
from typing import List, Optional, Union
from uuid import uuid4
from iqrfpy.utils.common import Common
from iqrfpy.enums.Commands import Command
from iqrfpy.enums.MessageTypes import MessageType
from iqrfpy.enums.peripherals import Peripheral

__all__ = ['IRequest']


@typechecked
class IRequest(ABC):
    __slots__ = '_nadr', '_pnum', '_pcmd', '_m_type', '_hwpid', '_pdata', '_msgid', '_params'

    def __init__(self, nadr: int, pnum: Peripheral, pcmd: Command, hwpid: int = Common.HWPID_MAX,
                 pdata: Optional[List[int]] = None, m_type: Optional[MessageType] = None, params: Optional[dict] = None,
                 msgid: str = str(uuid4())):
        self._nadr: int = nadr
        self._pnum: Peripheral = pnum
        self._pcmd: Command = pcmd
        self._hwpid: int = hwpid
        self._pdata: Optional[List[int]] = pdata
        self._m_type: Optional[str] = m_type.value if m_type is not None else m_type
        self._msgid: str = msgid
        self._params: Optional[dict] = params if params is not None else {}
        self._validate_base()

    def _validate_base(self) -> None:
        if self._nadr < 0 or self._nadr > 239:
            raise ValueError('NADR should be between 0 and 239.')
        if self._hwpid < 0 or self._hwpid > 65535:
            raise ValueError('HWPID should be between 0 and 65535.')

    @abstractmethod
    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._validate_base()
        dpa: List[int] = [0, self._nadr, self._pnum, self._pcmd, self._hwpid & 0xFF, (self._hwpid >> 8) & 0xFF]
        if self._pdata is not None:
            dpa.extend(self._pdata)
        if mutable:
            return bytearray(dpa)
        return bytes(dpa)

    @abstractmethod
    def to_json(self) -> dict:
        self._validate_base()
        return {
            'mType': self._m_type,
            'data': {
                'msgId': self._msgid,
                'req': {
                    'nAdr': self._nadr,
                    'hwpId': self._hwpid,
                    'param': self._params,
                },
                'returnVerbose': True,
            },
        }
