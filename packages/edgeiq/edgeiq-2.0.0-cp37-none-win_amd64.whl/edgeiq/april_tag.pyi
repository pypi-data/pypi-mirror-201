from _typeshed import Incomplete
from enum import Enum
from typing import NamedTuple

class _corner(NamedTuple):
    top_left: Incomplete
    top_right: Incomplete
    bottom_left: Incomplete
    bottom_right: Incomplete

class AprilTagFamily(Enum):
    TAG_16h5: Incomplete
    TAG_25h9: Incomplete
    TAG_36h10: Incomplete
    TAG_36h11: Incomplete

class AprilTagDetection:
    def __init__(self, top_right, top_left, bottom_right, bottom_left, tag_id) -> None: ...
    def markup_image(self, image, tag_id: bool = ...): ...
    @property
    def tag_id(self): ...
    @property
    def corners(self): ...

class AprilTagDetector:
    def __init__(self, family: AprilTagFamily) -> None: ...
    def detect(self, image): ...
