import threading
from .shared import Cmd as Cmd, ErrorRsp as ErrorRsp, InferenceBatchCmd as InferenceBatchCmd, InferenceCmd as InferenceCmd, LoadModelCmd as LoadModelCmd, Shared as Shared, StopCmd as StopCmd
from _typeshed import Incomplete
from edgeiq import ObjectDetection as ObjectDetection
from edgeiq.performance_analysis import FPS as FPS
from edgeiq.tools.hw_discovery import is_jetson as is_jetson

LOGGER: Incomplete

class ObjectDetectionInferenceThread(threading.Thread):
    def __init__(self, shared: Shared) -> None: ...
    def run(self) -> None: ...
    def close(self) -> None: ...
