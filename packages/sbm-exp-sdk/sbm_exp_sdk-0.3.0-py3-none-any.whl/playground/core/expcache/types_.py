import typing as tp
from collections.abc import Mapping, Sequence, Set
from dataclasses import is_dataclass

import numpy as np
import pandas as pd
import polars as pl
from scipy.sparse import coo_matrix, csc_matrix, csr_matrix

T = tp.TypeVar("T")


class LazyObject(tp.Generic[T]):
    data: tp.Optional[T]

    def __init__(self, path: str, _type: tp.Type) -> None:
        self.path = path
        self._type = _type
        self.data = None
        self.expcache_ref_cnt = 0

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"LazyObject(path='{self.path}', type={self._type})"


class Artifact:
    def __init__(self, obj: tp.Any) -> None:
        self.obj = obj
        if not is_registered_custom_type(obj.__class__):
            raise ValueError(f"{obj.__class__} is not supported as an artifact")

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Artifact(obj={repr(self.obj)})"


supported_primitive_types = (int, str, bool, float, bytes)

supported_numpy_types = (np.int8, np.int16, np.int32, np.int64, np.float16, np.float32, np.float64)

supported_custom_types = [pd.DataFrame, pl.DataFrame, np.ndarray, csr_matrix, coo_matrix, csc_matrix]


def is_supported_obj_type(obj: tp.Any, include_custom: bool = True) -> bool:
    condition = is_primitive_type(obj) or is_collection(obj) or is_dataclass(obj)
    return (condition and is_registered_custom_type(obj.__class__)) if include_custom else condition


def is_collection(obj: tp.Type) -> bool:
    return isinstance(obj, (Set, Sequence, Mapping))


def is_primitive_type(obj: tp.Type) -> bool:
    return isinstance(obj, supported_primitive_types)


def is_numpy_primitive_type(_type: tp.Type) -> bool:
    return any(_type == primitive_type for primitive_type in supported_numpy_types)


def is_registered_custom_type(_type: tp.Type) -> bool:
    return any(_type == custom_type for custom_type in supported_custom_types)
