import json

from typing import Callable, Optional
from paho.mqtt.client import Client
from iqrfpy.messages.requests.IRequest import IRequest
from iqrfpy.messages.responses.IResponse import IResponse
from iqrfpy.transports.itransport import ITransport


__all__ = ['MqttTransport']


class MqttTransport(ITransport):

    def __init__(self, host: str, port: int, client_id: str, request_topic: str, response_topic: str, user: str = None,
                 password: str = None, qos: int = 1):
        self._client = Client(client_id=client_id)
        self._host = host
        self._port = port
        self._request_topic = request_topic
        self._response_topic = response_topic
        self._user = user
        self._pass = password
        self._qos = qos
        self._callback: Optional[Callable] = None
        pass

    def initialize(self) -> None:
        self._client.on_connect = self.connect_callback
        self._client.on_message = self.message_callback
        if self._user is not None and self._pass is not None:
            self._client.username_pw_set(self._user, self._pass)
        self._client.connect(self._host, self._port)
        self._client.loop_start()

    def connect_callback(self, client, userdata, flags, rc):
        # pylint: disable=W0613
        if rc == 0:
            self._client.subscribe(self._response_topic, self._qos)

    def message_callback(self, client, userdata, message):
        # pylint: disable=W0613
        payload = json.loads(message.payload.decode('utf-8'))
        response = IResponse.from_json(payload)
        if self._callback is not None:
            self._callback(response)

    def send(self, request: IRequest) -> None:
        if self._client.is_connected():
            self._client.publish(topic=self._request_topic, payload=json.dumps(request.to_json()), qos=self._qos)

    def receive(self) -> IResponse:
        raise NotImplementedError('Synchronous communication not possible.')

    def receive_async(self, callback: Callable[[IResponse], None]) -> None:
        self._callback = callback
