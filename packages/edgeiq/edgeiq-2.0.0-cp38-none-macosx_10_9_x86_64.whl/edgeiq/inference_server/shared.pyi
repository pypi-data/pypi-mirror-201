import queue
from _typeshed import Incomplete
from edgeiq.engine_accelerator import Accelerator as Accelerator, Engine as Engine
from edgeiq.model_config.model_config import ModelConfig as ModelConfig
from edgeiq.object_detection import ObjectDetectionResults as ObjectDetectionResults
from typing import Any, List, Union

class ErrorRsp:
    msg: str
    def __init__(self, msg) -> None: ...
Rsp = Union[ErrorRsp, ObjectDetectionResults, List[ObjectDetectionResults], ModelConfig]

class InferenceCmd:
    frame: Any
    confidence_level: float
    overlap_threshold: float
    rsp_queue: queue.Queue[Rsp]
    def __init__(self, frame, confidence_level, overlap_threshold, rsp_queue) -> None: ...

class InferenceBatchCmd:
    frame: Any
    confidence_level: float
    overlap_threshold: float
    rsp_queue: queue.Queue[Rsp]
    def __init__(self, frame, confidence_level, overlap_threshold, rsp_queue) -> None: ...

class LoadModelCmd:
    model_id: str
    engine: Engine
    accelerator: Accelerator
    rsp_queue: queue.Queue[Rsp]
    def __init__(self, model_id, engine, accelerator, rsp_queue) -> None: ...

class StopCmd:
    stop: bool
    def __init__(self, stop) -> None: ...
Cmd = Union[InferenceCmd, LoadModelCmd, StopCmd]

class Shared:
    cmd_queue: Incomplete
    def __init__(self, max_cmd_queue_sz: int = ...) -> None: ...
