import numpy as np
from ..processor import Processor as Processor
from .hailo_processing import hailo_ssd_post_process as hailo_ssd_post_process, hailo_ssd_pre_process as hailo_ssd_pre_process, hailo_yolov3_post_process as hailo_yolov3_post_process, hailo_yolov3_pre_process as hailo_yolov3_pre_process
from .ocv_dnn import dnn_pre_process as dnn_pre_process, ssd_post_process as ssd_post_process, yolo_post_process as yolo_post_process
from .qaic_processing import qaic_yolo_post_process as qaic_yolo_post_process, qaic_yolo_post_process_batch as qaic_yolo_post_process_batch, qaic_yolo_pre_process as qaic_yolo_pre_process, qaic_yolo_pre_process_batch as qaic_yolo_pre_process_batch
from .tensor_rt import trt_ssd_post_process as trt_ssd_post_process, trt_ssd_pre_process as trt_ssd_pre_process, trt_yolo_post_process as trt_yolo_post_process, trt_yolo_post_process_batch as trt_yolo_post_process_batch, trt_yolo_pre_process as trt_yolo_pre_process, trt_yolo_pre_process_batch as trt_yolo_pre_process_batch
from .types import PostProcessBatchParams as PostProcessBatchParams, PostProcessParams as PostProcessParams, PreProcessBatchParams as PreProcessBatchParams, PreProcessParams as PreProcessParams
from _typeshed import Incomplete
from edgeiq.bounding_box import BoundingBox as BoundingBox
from edgeiq.model_config import ModelConfig as ModelConfig
from typing import Any, Callable, List, Tuple

PreProcessT: Incomplete
PreProcessBatchT: Incomplete
PostProcessT = Callable[[PostProcessParams], Tuple[List[BoundingBox], List[float], List[int]]]
PostProcessBatchT = Callable[[PostProcessBatchParams], Tuple[List[List[BoundingBox]], List[List[float]], List[List[int]]]]

class ObjectDetectionProcessor(Processor):
    def __init__(self, model_config: ModelConfig) -> None: ...
    def load(self) -> None: ...
    def pre_process(self, image: np.ndarray) -> np.ndarray: ...
    def pre_process_batch(self, images: List[np.ndarray]) -> np.ndarray: ...
    def post_process(self, results: Any, image: np.ndarray, confidence_level: float, overlap_threshold: float) -> Tuple[List[BoundingBox], List[float], List[int]]: ...
    def post_process_batch(self, results: List[Any], images: List[np.ndarray], confidence_level: float, overlap_threshold: float) -> Tuple[List[List[BoundingBox]], List[List[float]], List[List[int]]]: ...
