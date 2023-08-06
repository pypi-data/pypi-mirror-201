from ..constants import TO_CLOUD_TOPIC_PREFIX as TO_CLOUD_TOPIC_PREFIX
from ..credentials import CLIENT_ID as CLIENT_ID, CREDENTIALS_EXIST as CREDENTIALS_EXIST, ENDPOINT as ENDPOINT, PATH_TO_CERT as PATH_TO_CERT, PATH_TO_KEY as PATH_TO_KEY, PATH_TO_ROOT as PATH_TO_ROOT
from .base_connection import BaseCloudConnection as BaseCloudConnection
from _typeshed import Incomplete
from edgeiq.exceptions import PublishError as PublishError
from typing import Callable

queue_messages: Incomplete

class IoTCoreConnection(BaseCloudConnection):
    AT_LEAST_ONCE: Incomplete
    AT_MOST_ONCE: Incomplete
    def __new__(cls): ...
    mqtt_connection: Incomplete
    topic: Incomplete
    def __init__(self) -> None: ...
    def connect(self) -> None: ...
    def subscribe(self, topic: str, callback: Callable): ...
    def publish(self, message: str): ...
    def disconnect(self) -> None: ...
