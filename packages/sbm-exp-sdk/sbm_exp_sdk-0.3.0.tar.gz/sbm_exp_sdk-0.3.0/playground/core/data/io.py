from pickle import dump as pdump
from pickle import load as pload
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional, Sequence, Union

import pandas as pd
import polars as pl
from fsspec import AbstractFileSystem
from joblib import dump as jdump
from joblib import load as jload
from loguru import logger
from pyarrow import Table, parquet
from s3fs import S3FileSystem


def write_pickle(fs: AbstractFileSystem, obj: Any, path: str) -> None:
    logger.info(f"Saving {obj.__class__} to {path}")
    with fs.open(path, "wb") as f:
        pdump(obj, f)


def load_pickle(fs: AbstractFileSystem, path: str) -> Any:
    logger.info(f"Loading pickle object from {path}")
    with fs.open(path, "rb") as s3file:
        return pload(s3file)


def write_joblib(fs: AbstractFileSystem, obj: Any, path: str) -> None:
    logger.info(f"Saving {obj.__class__} to {path}")
    with fs.open(path, "wb") as f:
        jdump(obj, f)


def load_joblib(fs: AbstractFileSystem, path: str) -> Any:
    logger.info(f"Loading joblib object from {path}")
    with fs.open(path, "rb") as s3file:
        return jload(s3file)


def write_parquet(
    fs: AbstractFileSystem,
    df: Union[pd.DataFrame, pl.DataFrame],
    path: str,
    partition_cols: Optional[Sequence[str]] = None,
    overwrite: bool = True,
    **kwargs,
):
    """
    Запись в формате `Parquet` с использованием `pyarrow`.
    Может использоваться для записи партиционированного датасета.
    Для этого можно воспользоваться аргументом `partition_cols`, а можно передать этот ключ в `**kwargs`.
    :param df: таблица типа `pandas.DataFrame` или `polars.DataFrame`
    :param path: объектный путь типа /path/to/file или s3://bucket/path/to/file
    :param partition_cols: список полей для партиционирования
    :param overwrite: удалять ли существующие файлы перед записью.
        Следует передать `False` при многократной записи партиционированных датасетов по одному пути.
    :param kwargs: дополнительные аргументы для `pyarrow.parquet.write_to_dataset`
    :return:
    """
    table = df.to_arrow() if isinstance(df, pl.DataFrame) else Table.from_pandas(df)
    kwargs["partition_cols"] = kwargs.get("partition_cols") or partition_cols

    # this helps in the case of multiple saves to the same directory
    # otherwise parquet files from different attempts can mix
    if overwrite and fs.exists(path):
        logger.warning(f"Deleting existing {path} because the overwrite argument is set to True")
        fs.rm(path, recursive=True)

    parquet.write_to_dataset(table, root_path=path, filesystem=fs, **kwargs)

    logger.info(f"Written DataFrame {df.shape} to {path}")


def load_parquet(
    fs: AbstractFileSystem,
    path: str,
    columns: Optional[Union[Dict[str, Any], Sequence[str]]] = None,
    polars: bool = False,
) -> Union[pd.DataFrame, pl.DataFrame]:
    """
    Чтение датасета в формате `Parquet` с использованием `pyarrow`.
    Возвращает `polars.DataFrame. Для конвертации в `pandas.DataFrame` можно воспользоваться методом `df.to_pandas()`.
    :param path: объектный путь типа /path/to/file или s3://bucket/path/to/file
    :param columns: список полей для чтения (опционально)
    :param dataset_kwargs: дополнительные аргументы для `pyarrow.parquet.ParquetDataset`
    :param read_kwargs: дополнительные аргументы для `pyarrow.parquet.ParquetDataset.read`.
        В частности, при помощи этих аргументов можно прочитать только определенные партиции или колонки.
        Подробнее в документации `pyarrow`: https://arrow.apache.org/docs/python/dataset.html#reading-partitioned-data
    :return:
    """
    if columns is not None:
        column_names = columns.keys() if isinstance(columns, dict) else columns

    if isinstance(fs, S3FileSystem):
        with TemporaryDirectory() as temp_dir:
            fs.get(path, temp_dir, recursive=True)
            dataset = parquet.ParquetDataset(temp_dir)
            table = dataset.read(columns=column_names) if columns is not None else dataset.read()
    else:
        dataset = parquet.ParquetDataset(path)
        table = dataset.read(columns=column_names) if columns is not None else dataset.read()
    df = pl.from_arrow(table) if polars else table.to_pandas()

    if columns is not None and isinstance(columns, dict):
        if polars:
            df = df.select([pl.col(col).cast(col_type) for col, col_type in columns.items()])
        else:
            df = df.astype(columns)

    logger.info(f"Loaded DataFrame {df.shape} from {path}")

    return df
