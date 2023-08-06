from ..connection.iot_core_connection import IoTCoreConnection as IoTCoreConnection
from ..connection.rabbitmq_connection import RabbitMQConnection as RabbitMQConnection
from ..constants import PROJECT_ID as PROJECT_ID, RUN_RABBITMQ_CONNECTION as RUN_RABBITMQ_CONNECTION
from ..util import ProdClientError as ProdClientError, SerializableResultT as SerializableResultT, create_analytics_message_packet as create_analytics_message_packet
from .base_client import BaseClient as BaseClient
from _typeshed import Incomplete
from edgeiq.exceptions import PacketRateError as PacketRateError, PacketSizeError as PacketSizeError
from typing import Any

PUBLISH_RATE_LIMIT: Incomplete
PUBLISH_SIZE_LIMIT: Incomplete

class AnalyticsCloudWriter(BaseClient):
    cloud_connection: Incomplete
    exit_event: Incomplete
    def __init__(self) -> None: ...
    def publish_analytics(self, results: SerializableResultT, type: str, base_service: str, tag: Any = ...): ...
    def publish(self, message: str): ...
    def stop(self) -> None: ...
