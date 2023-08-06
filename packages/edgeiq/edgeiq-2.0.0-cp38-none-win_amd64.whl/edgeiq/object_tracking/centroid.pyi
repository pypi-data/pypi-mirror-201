from .matchers import match_greedy as match_greedy
from .object_tracking import DEFAULT_DEREGISTER_FRAMES as DEFAULT_DEREGISTER_FRAMES, DEFAULT_HISTORY_LENGTH as DEFAULT_HISTORY_LENGTH, DEFAULT_MAX_DISTANCE as DEFAULT_MAX_DISTANCE, DEFAULT_MIN_INERTIA as DEFAULT_MIN_INERTIA, PredictionT as PredictionT, TrackablePrediction as TrackablePrediction, TrackerAlgorithm as TrackerAlgorithm, TrackerCbT as TrackerCbT
from typing import Optional

class CentroidTracker(TrackerAlgorithm[TrackablePrediction]):
    def __init__(self, deregister_frames: int = ..., max_distance: int = ..., min_inertia: int = ..., history_length: int = ..., enter_cb: Optional[TrackerCbT] = ..., exit_cb: Optional[TrackerCbT] = ...): ...
