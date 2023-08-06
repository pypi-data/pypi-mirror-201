import tempfile
import typing
import uuid
from collections.abc import Mapping
from copy import deepcopy
from os.path import join

import joblib
import numpy as np
import pandas as pd
import polars as pl
from fsspec.implementations.local import LocalFileSystem
from loguru import logger
from playground.core.expcache.fs_utils import get_file_system_for_path
from playground.core.expcache.types_ import LazyObject
from s3fs import S3FileSystem
from scipy.sparse import coo_matrix, csc_matrix, csr_matrix, load_npz, save_npz, spmatrix


def _serialize(output: typing.Any, output_dir: str) -> str:
    fs = get_file_system_for_path(output_dir)
    if not fs.exists(output_dir):
        fs.mkdir(output_dir)
    if isinstance(fs, LocalFileSystem):
        object_name = uuid.uuid4().hex
        new_path = join(output_dir, object_name)
        new_path = SERIALIZERS[output.__class__](output, new_path)
        return new_path
    elif isinstance(fs, S3FileSystem):
        with tempfile.TemporaryDirectory() as tdir:
            object_name = uuid.uuid4().hex
            tpath = join(tdir, object_name)
            logger.info(f"Serializing to {tpath} locally")
            tpath = SERIALIZERS[output.__class__](output, tpath)
            new_path = f"{output_dir}/{object_name}"
            logger.info(f"Moving {tpath} to {new_path}")
            fs.put(tpath, new_path)
            return new_path
    else:
        raise ValueError(f"Unknown filesystem {fs}")


def deserialize(data: typing.Any) -> typing.Any:
    container = deepcopy(data)

    def deserializator(container: typing.Any) -> typing.Any:
        if isinstance(container, LazyObject):
            return _deserialize(container)
        if isinstance(container, Mapping):
            for key in container:
                if isinstance(container[key], LazyObject):
                    container[key] = _deserialize(container[key])  # type: ignore
                else:
                    container[key] = deserialize(container[key])  # type: ignore
        elif isinstance(container, typing.Sequence):
            for idx in range(len(container)):
                if isinstance(container[idx], LazyObject):
                    container[idx] = _deserialize(container[idx])  # type: ignore
                else:
                    container[idx] = deserialize(container[idx])  # type: ignore
        return container

    return deserializator(container=container)


def _deserialize(lazy_object: LazyObject) -> typing.Any:
    fs = get_file_system_for_path(lazy_object.path)
    if isinstance(fs, LocalFileSystem):
        return DESERIALIZERS[lazy_object._type](lazy_object.path)
    elif isinstance(fs, S3FileSystem):
        with tempfile.NamedTemporaryFile() as tfile:
            fs.get(lazy_object.path, tfile.name)
            return DESERIALIZERS[lazy_object._type](tfile.name)
    else:
        raise ValueError(f"Unknown filesystem {fs}")


def pandas_dataframe_serializer(dataframe: pd.DataFrame, path: str) -> str:
    dataframe.to_parquet(path)
    return path


def pandas_dataframe_deserializer(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def polars_dataframe_serializer(dataframe: pl.DataFrame, path: str) -> str:
    dataframe.write_parquet(path)
    return path


def polars_dataframe_deserializer(path: str) -> pl.DataFrame:
    return pl.read_parquet(path)


def numpy_serializer(np_arr: np.ndarray, path: str) -> str:
    np.save(path, np_arr)
    return f"{path}.npy"


def numpy_deserializer(path: str) -> np.ndarray:
    return np.load(path)  # type: ignore


def scipy_mat_serializer(mat: spmatrix, path: str) -> str:
    save_npz(path, mat)
    return f"{path}.npz"


def scipy_mat_deserializer(path: str) -> spmatrix:
    return load_npz(path)


def joblib_serializer(obj: typing.Any, path: str) -> str:
    with open(path, "wb") as f:
        joblib.dump(obj, f)
    return path


def joblib_deserializer(path) -> typing.Any:
    with open(path, "rb") as f:
        return joblib.load(f)


SERIALIZERS = {
    pl.DataFrame: polars_dataframe_serializer,  # type: ignore
    pd.DataFrame: pandas_dataframe_serializer,
    np.ndarray: numpy_serializer,
    coo_matrix: scipy_mat_serializer,
    csr_matrix: scipy_mat_serializer,
    csc_matrix: scipy_mat_serializer,
}

DESERIALIZERS = {
    pl.DataFrame: polars_dataframe_deserializer,
    pd.DataFrame: pandas_dataframe_deserializer,
    np.ndarray: numpy_deserializer,
    coo_matrix: scipy_mat_deserializer,
    csr_matrix: scipy_mat_deserializer,
    csc_matrix: scipy_mat_deserializer,
}
