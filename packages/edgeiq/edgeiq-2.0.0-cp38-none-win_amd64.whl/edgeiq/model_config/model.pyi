from _typeshed import Incomplete
from typing import Union

data_dir: Incomplete
catalog: Incomplete
hailoModel: Incomplete
qaicModel: Incomplete
modelParameters: Incomplete
modelJson: Incomplete

class ModelJson:
    accuracy: Incomplete
    dataset: Incomplete
    description: Incomplete
    id: Incomplete
    inference_time: Incomplete
    license: Incomplete
    mean_average_precision_top_1: Incomplete
    mean_average_precision_top_5: Incomplete
    public: Incomplete
    website_url: Incomplete
    model_parameters: Incomplete
    def __init__(self, accuracy: Union[str, None], dataset: str, description: str, id: str, inference_time: Union[int, None], license: str, mean_average_precision_top_1: Union[int, None], mean_average_precision_top_5: Union[int, None], public: Union[bool, None], website_url: str, model_parameters: object) -> None: ...

def validateModel(model_config: ModelJson): ...
