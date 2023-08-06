from _typeshed import Incomplete
from enum import Enum

APP_ROOT: Incomplete
MODELS_DIR: Incomplete
CREDENTIALS_DIR: Incomplete
NCS2_VID: int
NCS2_PID: int
HAILO_VID: str
HAILO_PID: str
CUDA_SUPPORTED_BOARDS: Incomplete
TEGRA_CHIP_PATH: str
CPU_COUNT_PATH: str
MYRIAD_SUPPORTED_OS: Incomplete
HAILO_SUPPORTED_OS: Incomplete
QAIC_SUPPORTED_OS: Incomplete
EYECLOUD_SUPPORTED_MODEL_PURPOSES: Incomplete

class SupportedDevices(str, Enum):
    EYECLOUD: str
    OAK: str
    NANO: str
    XAVIER_NX: str
    AGX_XAVIER: str

DISABLE_VALIDATION: Incomplete
EYECLOUD_LIB_DIR: Incomplete
EDGEIQ_LOGS: Incomplete
