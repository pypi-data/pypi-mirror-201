import numpy as np
from .processor import Processor
from edgeiq.model_config import ModelConfig
from edgeiq.pose_estimation_pose import Pose
from typing import Any, Callable, List, Tuple

class PreProcessParams:
    image: np.ndarray
    size: Tuple[int, int]
    scalefactor: float
    mean: Tuple[float, float, float]
    swaprb: bool
    crop: bool
    def __init__(self, image, size, scalefactor, mean, swaprb, crop) -> None: ...

class PostProcessParams:
    results: Any
    image: np.ndarray
    def __init__(self, results, image) -> None: ...
PostProcessT = Callable[[PostProcessParams], List[Pose]]

class PoseEstimationProcessor(Processor):
    def __init__(self, model_config: ModelConfig) -> None: ...
    def load(self) -> None: ...
    def pre_process(self, image: np.ndarray) -> np.ndarray: ...
    def post_process(self, results: Any, image: np.ndarray) -> List[Pose]: ...
