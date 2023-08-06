from edgeiq.bounding_box import BoundingBox as BoundingBox
from edgeiq.object_detection import ObjectDetectionPrediction as ObjectDetectionPrediction
from typing import Optional, Tuple

def parse_cvat_annotations(path: str, start_frame: int = ..., end_frame: Optional[int] = ..., new_id_for_occlusion: bool = ...) -> Tuple[dict, dict]: ...
