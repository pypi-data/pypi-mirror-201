from edgeiq._globals import USERNAME as USERNAME
from edgeiq._production_client.credentials import CLIENT_ID as CLIENT_ID
from edgeiq.app_config import AppConfig as AppConfig
from typing import Any

SerializableResultT = Any

class ProdClientError(Exception): ...

def create_analytics_message_packet(results: SerializableResultT, type: str, base_service: str, tag: Any = ...): ...
