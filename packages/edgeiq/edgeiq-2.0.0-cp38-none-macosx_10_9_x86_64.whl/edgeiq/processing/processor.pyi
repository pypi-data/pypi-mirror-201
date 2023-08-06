from edgeiq.model_config.model_config import ModelConfig as ModelConfig
from typing import TypeVar

class Processor:
    def __init__(self, model_config: ModelConfig) -> None: ...
    def load(self) -> None: ...
ProcessorT = TypeVar('ProcessorT', bound=Processor)
