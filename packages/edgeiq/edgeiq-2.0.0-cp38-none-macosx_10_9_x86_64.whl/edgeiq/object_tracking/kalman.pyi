import numpy as np
from .matchers import match_greedy as match_greedy
from .object_tracking import DEFAULT_DEREGISTER_FRAMES as DEFAULT_DEREGISTER_FRAMES, DEFAULT_HISTORY_LENGTH as DEFAULT_HISTORY_LENGTH, DEFAULT_MAX_DISTANCE as DEFAULT_MAX_DISTANCE, DEFAULT_MIN_INERTIA as DEFAULT_MIN_INERTIA, PredictionT as PredictionT, TrackablePrediction as TrackablePrediction, TrackerAlgorithm as TrackerAlgorithm, TrackerCbT as TrackerCbT
from _typeshed import Incomplete
from typing import Optional

class TrackableKalmanPrediction(TrackablePrediction):
    filter: Incomplete
    dim_x: Incomplete
    dim_z: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def estimated_position(self) -> np.ndarray: ...
    @property
    def estimated_velocity(self) -> np.ndarray: ...
    def step(self, *args, **kwargs) -> None: ...
    def handle_found(self, prediction: PredictionT): ...

class KalmanTracker(TrackerAlgorithm[TrackableKalmanPrediction]):
    def __init__(self, deregister_frames: int = ..., max_distance: int = ..., min_inertia: int = ..., history_length: int = ..., enter_cb: Optional[TrackerCbT] = ..., exit_cb: Optional[TrackerCbT] = ...): ...
