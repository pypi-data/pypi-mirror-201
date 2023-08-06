import numpy as np
from .matchers import match_greedy as match_greedy
from .object_tracking import DEFAULT_DEREGISTER_FRAMES as DEFAULT_DEREGISTER_FRAMES, DEFAULT_HISTORY_LENGTH as DEFAULT_HISTORY_LENGTH, DEFAULT_MAX_DISTANCE as DEFAULT_MAX_DISTANCE, DEFAULT_MIN_INERTIA as DEFAULT_MIN_INERTIA, PredictionT as PredictionT, TrackablePrediction as TrackablePrediction, TrackerAlgorithm as TrackerAlgorithm, TrackerCbT as TrackerCbT, TrackingResults as TrackingResults
from enum import Enum
from typing import Callable, List, Optional

class TrackingState(Enum):
    DETECT: str
    REDETECT: str

class TrackableCorrelationPrediction(TrackablePrediction):
    def __init__(self, *args, **kwargs) -> None: ...
    def handle_found(self, prediction: PredictionT, dereg_tracked_obj: Callable[[], None], **kwargs): ...
    def handle_disappeared(self, image: np.ndarray, reg_tracked_obj: Callable[[], None], can_track_new_obj: Callable[[], bool], **kwargs): ...

class CorrelationTracker(TrackerAlgorithm[TrackableCorrelationPrediction]):
    def __init__(self, max_objects: int = ..., deregister_frames: int = ..., max_distance: int = ..., min_inertia: int = ..., history_length: int = ..., enter_cb: Optional[TrackerCbT] = ..., exit_cb: Optional[TrackerCbT] = ...): ...
    def update(self, predictions: List[PredictionT], image: np.ndarray) -> TrackingResults: ...
