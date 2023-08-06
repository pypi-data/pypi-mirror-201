from .clients import AnalyticsCloudWriter as AnalyticsCloudWriter, AnalyticsFileWriter as AnalyticsFileWriter, ClientManager as ClientManager, ImageCloudWriter as ImageCloudWriter
from _typeshed import Incomplete
from edgeiq.app_config import AppConfig as AppConfig

PRODUCTION_CLIENT: Incomplete
app_cfg: Incomplete

def initialize_clients() -> None: ...
