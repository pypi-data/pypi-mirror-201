import numpy as np
from _typeshed import Incomplete
from enum import Enum
from typing import List

class MOG2:
    cuda: Incomplete
    history: Incomplete
    var_threshold: Incomplete
    detect_shadows: Incomplete
    bgmog2: Incomplete
    def __init__(self, history: int = ..., var_threshold: int = ..., detect_shadows: bool = ..., cuda: bool = ...) -> None: ...
    frame: Incomplete
    def process_frame(self, frame, learning_rate: int = ...): ...

def get_contours(raw_contours): ...
def get_boundingboxes(contours): ...
def get_moments(contours): ...

class SortingMethod(Enum):
    LEFT_RIGHT: str
    RIGHT_LEFT: str
    BOTTOM_TOP: str
    TOP_BOTTOM: str

def get_sorted(method: SortingMethod, contours: List[np.ndarray]): ...
