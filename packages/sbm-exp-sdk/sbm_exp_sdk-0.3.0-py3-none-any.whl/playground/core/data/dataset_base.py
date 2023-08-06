import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union, cast

import pandas as pd
import polars as pl
from playground.core.s3_source.base import S3Source
from s3fs import S3FileSystem


class Dataset:
    __load_args__: List[str]

    def __init__(
        self,
        path: str,
        source: S3Source,
        date_format: str = "%Y-%m-%d",
        key: Optional[Sequence[str]] = None,
    ):
        self._path = path
        self._source = source
        self._key = key
        self._date_format = date_format

    def _check_load_args(self, load_args: Dict[str, Any]) -> None:
        for field in self.__load_args__:
            if field not in load_args:
                raise KeyError(f"{field} data argument is not specified")

    def get_path(self, date: datetime) -> str:
        return os.path.join("s3://", self.bucket, self._path, f"date={date.strftime(self.date_format)}")

    @property
    def fs(self) -> S3FileSystem:
        return self._source.fs

    @property
    def key(self) -> List[str]:
        return cast(List[str], self._key) if self._key else []

    @property
    def date_format(self) -> str:
        return self._date_format

    @property
    def bucket(self) -> str:
        return self._source.bucket

    def load(
        self, polars: bool, load_args: Dict[str, Any], keys: Union[pl.DataFrame, pd.DataFrame]
    ) -> Union[pl.DataFrame, pd.DataFrame]:
        raise NotImplementedError("load is not implemented")
