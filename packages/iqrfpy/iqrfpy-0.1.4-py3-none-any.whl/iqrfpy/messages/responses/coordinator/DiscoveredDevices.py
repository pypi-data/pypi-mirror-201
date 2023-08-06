from __future__ import annotations
from typeguard import typechecked
from typing import List, Optional
from iqrfpy.enums.Commands import CoordinatorResponseCommands
from iqrfpy.enums.MessageTypes import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
from iqrfpy.messages.responses.IResponse import IResponse, IResponseGetterMixin

__all__ = ['DiscoveredDevicesResponse']


@typechecked
class DiscoveredDevicesResponse(IResponseGetterMixin):
    __slots__ = '_discovered'

    def __init__(self, hwpid: int = Common.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=0,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorResponseCommands.DISCOVERED_DEVICES,
            m_type=CoordinatorMessages.DISCOVERED_DEVICES,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        if rcode == 0:
            self._discovered = result['discoveredDevices']

    def get_discovered(self) -> List[int]:
        return self._discovered

    @staticmethod
    def from_dpa(dpa: bytes) -> DiscoveredDevicesResponse:
        IResponse.validate_dpa_response(dpa)
        hwpid = Common.hwpid_from_dpa(dpa[5], dpa[4])
        rcode = dpa[6]
        result = None
        if rcode == 0:
            if len(dpa) != 40:
                raise ValueError('Response packet incomplete.')
            result = {'discoveredDevices': Common.bitmap_to_nodes(list(dpa[8:]))}
        return DiscoveredDevicesResponse(hwpid=hwpid, rcode=rcode, dpa_value=dpa[7], result=result)

    @staticmethod
    def from_json(json: dict) -> DiscoveredDevicesResponse:
        msgid = Common.msgid_from_json(json)
        hwpid = Common.hwpid_from_json(json)
        dpa_value = Common.dpa_value_from_json(json)
        rcode = Common.rcode_from_json(json)
        result = Common.result_from_json(json) if rcode == 0 else None
        return DiscoveredDevicesResponse(msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
