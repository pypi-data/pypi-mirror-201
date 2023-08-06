from iqrfpy.messages.requests.coordinator import *
from iqrfpy.transports.itransport import ITransport
from iqrfpy.messages.requests.coordinator.AuthorizeBond import AuthorizeBondParams

trans = ITransport()

trans.receive()

data = [
    AuthorizeBondParams(reqAddr=1, mid=0),
    AuthorizeBondParams(reqAddr=2, mid=2164554855),
    AuthorizeBondParams(reqAddr=3, mid=2164554771),
]
request = AuthorizeBondRequest(data)
print(request.to_dpa())
print(request.to_json())

request = BondNodeRequest(req_addr=1, bonding_test_retries=3)
dpa = request.to_dpa()

transport = ITransport()
transport.send(request=request)

while True:
    response = transport.receive()
    ...

