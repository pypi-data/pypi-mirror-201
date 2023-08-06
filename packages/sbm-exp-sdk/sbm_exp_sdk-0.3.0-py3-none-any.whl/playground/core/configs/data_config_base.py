from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class RawDataConfig:
    dataset_alias_to_load_config: Dict[str, Dict[str, Any]]

    @staticmethod
    def test_instance(date: datetime):
        raise NotImplementedError("test_instance is not implemented")

    @staticmethod
    def prod_instance(date: datetime):
        raise NotImplementedError("test_instance is not implemented")
