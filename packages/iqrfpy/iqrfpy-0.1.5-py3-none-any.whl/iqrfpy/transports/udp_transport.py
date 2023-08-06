from enum import IntEnum
import socket
from typing import Callable
from crc import Calculator, Crc16
from iqrfpy.messages.requests.IRequest import IRequest
from iqrfpy.messages.responses.IResponse import IResponse
from iqrfpy.transports.itransport import ITransport

__all__ = ['UdpTransport', 'UdpPacketHeader']

BUF_SIZE = 1024
CMD_WRITE_DATA = 0x03
RESERVED = 0x00


class UdpPacketHeader(IntEnum):
    """
    UDP packet header member enum.
    """
    GW_ADDR = 0
    CMD = 1
    SUBCMD = 2
    RES0 = 3
    RES1 = 4
    PACKET_ID_H = 5
    PACKET_ID_L = 6
    DATA_LEN_H = 7
    DATA_LEN_L = 8


class UdpTransport(ITransport):
    __slots__ = '_local_host', '_local_port', '_remote_host', '_remote_port', '_sender', '_listener', '_packet_id', '_gw_id'

    GATEWAY_IQRF = 0x22
    GATEWAY_USER = 0x20
    HEADER_LEN = 9
    DATA_MAX_LEN = 497
    CRC_LEN = 2

    def __init__(self, local_host: str, local_port: int, remote_host: str, remote_port: int, gw_id: int):
        self._sender = None
        self._listener = None
        self._local_host: str = local_host
        self._local_port: int = local_port
        self._remote_host: str = remote_host
        self._remote_port: int = remote_port
        self._packet_id: int = 0
        self._gw_id: int = gw_id

    def initialize(self):
        self._sender: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        self._listener: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        self._listener.bind((self._local_host, self._local_port))

    def send(self, request: IRequest) -> None:
        message = self._encode_packet(request.to_dpa(mutable=True))
        self._sender.sendto(message, (self._remote_host, self._remote_port))
        self._packet_id += 1

    def receive(self) -> IResponse:
        data, _ = self._listener.recvfrom(BUF_SIZE)
        print(data)
        self._decode_packet(data)
        return IResponse.from_dpa(data)

    def receive_async(self, callback: Callable[[IResponse], None]) -> None:
        data, _ = self._sender.recvfrom(BUF_SIZE)
        callback(IResponse.from_dpa(data))

    def _encode_packet(self, data: bytearray) -> bytes:
        data_len = len(data)
        message = bytearray([
            self._gw_id,
            CMD_WRITE_DATA,
            0x00,
            RESERVED,
            RESERVED,
            (self._packet_id >> 8) & 0xFF,
            self._packet_id & 0xFF,
            (data_len >> 8) & 0xFF,
            data_len & 0xFF]
        )
        message.extend(data)
        checksum = self._calculate_crc16_ccitt(message)
        message.extend(bytearray([(checksum >> 8) & 0xFF, checksum & 0xFF]))
        return message

    def _decode_packet(self, data: bytes) -> None:
        if len(data) < (self.HEADER_LEN + self.CRC_LEN):
            raise ValueError('UDP packet too short.')
        if len(data) > (self.HEADER_LEN + self.DATA_MAX_LEN + self.CRC_LEN):
            raise ValueError('UDP packet too long.')
        if data[UdpPacketHeader.GW_ADDR] != self._gw_id:
            raise ValueError('Identification address mismatch.')
        header_data_len = (data[UdpPacketHeader.DATA_LEN_H] << 8) + data[UdpPacketHeader.DATA_LEN_L]
        if header_data_len != (len(data) - self.HEADER_LEN - self.CRC_LEN):
            raise ValueError('Header data length does not match real data length.')
        header_crc = (data[-2] << 8) + data[-1]
        if header_crc != self._calculate_crc16_ccitt(data[-2:]):
            raise ValueError('Header checksum does not match real checksum.')

    @staticmethod
    def _calculate_crc16_ccitt(data: bytes):
        calculator = Calculator(Crc16.CCITT.value, optimized=True)
        return calculator.checksum(data)
