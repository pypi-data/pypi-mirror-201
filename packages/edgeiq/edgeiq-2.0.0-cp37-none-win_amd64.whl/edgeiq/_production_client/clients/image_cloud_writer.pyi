import numpy as np
from ..connection.iot_core_connection import IoTCoreConnection as IoTCoreConnection
from ..constants import DEVICE_TAG as DEVICE_TAG, IMAGE_TYPE as IMAGE_TYPE, PROJECT_TAG as PROJECT_TAG, TOPIC_PREFIX as TOPIC_PREFIX
from ..credentials import CLIENT_ID as CLIENT_ID
from ..util import ProdClientError as ProdClientError
from .base_client import BaseClient as BaseClient
from _typeshed import Incomplete
from edgeiq.app_config import AppConfig as AppConfig
from typing import Any

class ImageCloudWriter(BaseClient):
    cloud_connection: Incomplete
    publish_topic: Incomplete
    subscribe_url_response_topic: Incomplete
    exit_event: Incomplete
    images: Incomplete
    def __init__(self) -> None: ...
    def publish_image(self, image: np.ndarray, tag: Any = ...): ...
    def publish(self, message: str, topic: str): ...
    def stop(self) -> None: ...
