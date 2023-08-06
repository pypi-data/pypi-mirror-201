import unittest
from dataclasses import dataclass
from typing import Union
from parameterized import parameterized
from iqrfpy.messages.requests.coordinator.SmartConnect import SmartConnectRequest


@dataclass
class DataRegular:
    req_addr = 10
    bonding_test_retries = 3
    ibk = '201c5e762f75d7e244c3fa09b3de0ea1'
    mid = 2165321045
    virtual_device_address = 255
    expected_ibk = [32, 28, 94, 118, 47, 117, 215, 226, 68, 195, 250, 9, 179, 222, 14, 161]
    expected_dpa = b''.join([
        b'\x00\x00\x00\x12\xff\xff\x0a\x03\x20\x1c\x5e\x76\x2f\x75\xd7\xe2\x44\xc3\xfa\x09\xb3\xde\x0e\xa1\x55'
        b'\x2d\x10\x81\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ])


class DataTempAddr:
    req_addr = 254
    bonding_test_retries = 0
    ibk = '6ff99d9b506cce28ab47aee7c8215392'
    mid = 0
    virtual_device_address = 0
    expected_ibk = [111, 249, 157, 155, 80, 108, 206, 40, 171, 71, 174, 231, 200, 33, 83, 146]
    expected_dpa = b''.join([
        b'\x00\x00\x00\x12\xff\xff\xfe\x00\x6f\xf9\x9d\x9b\x50\x6c\xce\x28\xab\x47\xae\xe7\xc8\x21\x53\x92\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ])


class SmartConnectRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b''.join([
            b'\x00\x00\x00\x12\xff\xff\x0b\x01\x9a\x69\x1f\x1a\x21\x01\x21\x65\x03\xe5\xc5\x88\xff\xe7\xf6\xc2\x55',
            b'\x2d\x10\x81\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ])
        self.json = {
            'mType': 'iqrfEmbedCoordinator_SmartConnect',
            'data': {
                'msgId': 'smartConnectTest',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {
                        'reqAddr': 11,
                        'bondingTestRetries': 1,
                        'ibk': [
                            154,
                            105,
                            31,
                            26,
                            33,
                            1,
                            33,
                            101,
                            3,
                            229,
                            197,
                            136,
                            255,
                            231,
                            246,
                            194
                        ],
                        'mid': 2165321045,
                        'virtualDeviceAddress': 255,
                        'userData': [
                            0,
                            0,
                            0,
                            0
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        ['regular', DataRegular],
        ['temporary_addr', DataTempAddr]
    ])
    def test_to_dpa(self, _, data: Union[DataRegular, DataTempAddr]):
        request = SmartConnectRequest(
            req_addr=data.req_addr,
            bonding_test_retries=data.bonding_test_retries,
            ibk=data.ibk,
            mid=data.mid,
            virtual_device_address=data.virtual_device_address
        )
        print(request.to_dpa())
        print(data.expected_dpa)
        self.assertEqual(
            request.to_dpa(),
            data.expected_dpa
        )

    @parameterized.expand([
        ['regular', DataRegular],
        ['temporary_addr', DataTempAddr]
    ])
    def test_to_json(self, _, data: Union[DataRegular, DataTempAddr]):
        request = SmartConnectRequest(
            req_addr=data.req_addr,
            bonding_test_retries=data.bonding_test_retries,
            ibk=data.ibk,
            mid=data.mid,
            virtual_device_address=data.virtual_device_address,
            msgid='smartConnectTest'
        )
        self.json['data']['req']['param']['reqAddr'] = data.req_addr
        self.json['data']['req']['param']['bondingTestRetries'] = data.bonding_test_retries
        self.json['data']['req']['param']['ibk'] = data.expected_ibk
        self.json['data']['req']['param']['mid'] = data.mid
        self.json['data']['req']['param']['virtualDeviceAddress'] = data.virtual_device_address
        print(request.to_json())
        print(self.json)
        self.assertEqual(
            request.to_json(),
            self.json
        )

    def test_set_req_addr(self):
        request = SmartConnectRequest(
            req_addr=self.json['data']['req']['param']['reqAddr'],
            bonding_test_retries=self.json['data']['req']['param']['bondingTestRetries'],
            ibk='9a691f1a2101216503e5c588ffe7f6c2',
            mid=self.json['data']['req']['param']['mid'],
            virtual_device_address=self.json['data']['req']['param']['virtualDeviceAddress'],
            msgid='smartConnectTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.set_req_addr(DataRegular.req_addr)
        self.json['data']['req']['param']['reqAddr'] = DataRegular.req_addr
        dpa = list(self.dpa)
        dpa[6] = DataRegular.req_addr
        dpa = bytes(dpa)
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    def test_set_bonding_test_retries(self):
        request = SmartConnectRequest(
            req_addr=self.json['data']['req']['param']['reqAddr'],
            bonding_test_retries=self.json['data']['req']['param']['bondingTestRetries'],
            ibk='9a691f1a2101216503e5c588ffe7f6c2',
            mid=self.json['data']['req']['param']['mid'],
            virtual_device_address=self.json['data']['req']['param']['virtualDeviceAddress'],
            msgid='smartConnectTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.set_bonding_test_retries(DataRegular.bonding_test_retries)
        self.json['data']['req']['param']['bondingTestRetries'] = DataRegular.bonding_test_retries
        dpa = list(self.dpa)
        dpa[7] = DataRegular.bonding_test_retries
        dpa = bytes(dpa)
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    def test_set_ibk(self):
        request = SmartConnectRequest(
            req_addr=self.json['data']['req']['param']['reqAddr'],
            bonding_test_retries=self.json['data']['req']['param']['bondingTestRetries'],
            ibk='9a691f1a2101216503e5c588ffe7f6c2',
            mid=self.json['data']['req']['param']['mid'],
            virtual_device_address=self.json['data']['req']['param']['virtualDeviceAddress'],
            msgid='smartConnectTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.set_ibk(DataRegular.ibk)
        self.json['data']['req']['param']['ibk'] = DataRegular.expected_ibk
        dpa = list(self.dpa)
        dpa = dpa[:8] + DataRegular.expected_ibk + dpa[24:]
        dpa = bytes(dpa)
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    def test_set_mid(self):
        request = SmartConnectRequest(
            req_addr=self.json['data']['req']['param']['reqAddr'],
            bonding_test_retries=self.json['data']['req']['param']['bondingTestRetries'],
            ibk='9a691f1a2101216503e5c588ffe7f6c2',
            mid=self.json['data']['req']['param']['mid'],
            virtual_device_address=self.json['data']['req']['param']['virtualDeviceAddress'],
            msgid='smartConnectTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.set_mid(DataRegular.mid)
        self.json['data']['req']['param']['mid'] = DataRegular.mid
        dpa_mid = [
            DataRegular.mid & 0xFF,
            (DataRegular.mid >> 8) & 0xFF,
            (DataRegular.mid >> 16) & 0xFF,
            (DataRegular.mid >> 24) & 0xFF
        ]
        dpa = list(self.dpa)
        dpa = dpa[:24] + dpa_mid + dpa[28:]
        dpa = bytes(dpa)
        print(request.to_dpa())
        print(dpa)
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    def test_set_virtual_device_address(self):
        request = SmartConnectRequest(
            req_addr=self.json['data']['req']['param']['reqAddr'],
            bonding_test_retries=self.json['data']['req']['param']['bondingTestRetries'],
            ibk='9a691f1a2101216503e5c588ffe7f6c2',
            mid=self.json['data']['req']['param']['mid'],
            virtual_device_address=self.json['data']['req']['param']['virtualDeviceAddress'],
            msgid='smartConnectTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.set_virtual_device_address(DataRegular.virtual_device_address)
        self.json['data']['req']['param']['virtualDeviceAddress'] = DataRegular.virtual_device_address
        dpa = list(self.dpa)
        dpa[29] = DataRegular.virtual_device_address
        dpa = bytes(dpa)
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        ['req_addr', 0, 0, '', 0, 0],
        ['req_addr', 250, 0, '', 0, 0],
        ['bonding_test_retries', 1, -1, '', 0, 0],
        ['bonding_test_retries', 1, 270, '', 0, 0],
        ['ibk', 1, 1, 'a', 0, 0],
        ['ibk', 1, 1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaax', 0, 0],
        ['mid', 1, 1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', -1, 0],
        ['mid', 1, 1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 4294967298, 0],
        ['virtual_device_address', 1, 1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 0, 0],
        ['virtual_device_address', 1, 1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 0, 250],
        ['temp_addr_bonding_test_retries', 254, 2, '', 0, 0],
        ['temp_addr_ibk', 254, 0, 'aaaaaaaaa', 5, 0],
        ['temp_addr_ibk', 254, 0, '00000000000000000000000000000000000a', 0, 0],
        ['temp_addr_mid', 254, 0, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 5, 0],
        ['temp_addr_vrn', 254, 0, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 0, 10]
    ])
    def test_construct_invalid(self, _, req_addr, bonding_test_retries, ibk, mid, virtual_device_address):
        with self.assertRaises(ValueError):
            SmartConnectRequest(
                req_addr=req_addr,
                bonding_test_retries=bonding_test_retries,
                ibk=ibk,
                mid=mid,
                virtual_device_address=virtual_device_address
            )
