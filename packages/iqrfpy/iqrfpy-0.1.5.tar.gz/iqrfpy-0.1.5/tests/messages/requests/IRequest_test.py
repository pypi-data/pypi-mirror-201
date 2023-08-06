import unittest
from parameterized import parameterized
from iqrfpy.messages.requests.coordinator.AddrInfo import AddrInfoRequest
from iqrfpy.messages.requests.node.Read import ReadRequest


class IRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = AddrInfoRequest(msgid='addrInfoTest')
        self.json = {
            'mType': 'iqrfEmbedCoordinator_AddrInfo',
            'data': {
                'msgId': 'test',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {},
                },
                'returnVerbose': True
            },
        }

    @parameterized.expand([
        ['immutable', False, b'\x00\x00\x00\x00\xff\xff'],
        ['mutable', True, bytearray(b'\x00\x00\x00\x00\xff\xff')]
    ])
    def test_to_dpa(self, _, mutable, expected):
        self.assertEqual(
            self.request.to_dpa(mutable),
            expected
        )

    @parameterized.expand([
        ['nadr_low', -1, 65535],
        ['nadr_high', 1000, 65535],
        ['hwpid_low', 1, -10],
        ['hwpid_high', 1, 100000]
    ])
    def test_validate_base_invalid(self, _, nadr, hwpid):
        with self.assertRaises(ValueError):
            ReadRequest(nadr=nadr, hwpid=hwpid)
