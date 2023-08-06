from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, Optional, Union, cast

import pandas as pd
import polars as pl
from playground.core.data.dataset_base import Dataset
from playground.core.data.io import load_parquet


class ParquetDataset(Dataset):
    __load_args__ = ["date"]

    def load(
        self,
        polars: bool,
        load_args: Dict[str, Any],
        keys: Optional[Union[pl.DataFrame, pd.DataFrame]] = None,
    ) -> Union[pl.DataFrame, pd.DataFrame]:
        self._check_load_args(load_args=load_args)

        load_date: datetime = load_args["date"]
        load_path = self.get_path(date=load_date)

        columns_arg = None
        if "columns" in load_args and isinstance(load_args["columns"], Mapping):
            load_args = deepcopy(load_args)
            columns_arg = load_args["columns"]
            load_args["columns"] = list(columns_arg.keys())
        load_args = {key: value for key, value in load_args.items() if key not in self.__load_args__}

        data = load_parquet(fs=self.fs, path=load_path, polars=polars, **load_args)
        if "frac" in load_args:
            data = data.sample(frac=load_args["frac"])

        if columns_arg is not None:
            if polars:
                data = cast(pl.DataFrame, data)
                data = data.select([pl.col(col).cast(dtype) for col, dtype in columns_arg.items()])
            else:
                data = cast(pd.DataFrame, data)
                data = data.astype(columns_arg)

        if keys is not None:
            if polars:
                data = cast(pl.DataFrame, data)
                data = data.join(keys, on=keys.columns, how="inner")
            else:
                data = cast(pd.DataFrame, data)
                data = data.merge(keys, on=keys.columns, how="inner")

        return data


class DatePartitionedParquetDataset(Dataset):
    __load_args__ = ["from_date", "to_date"]
    __extra_args__ = ["n_partitions"]

    def get_last_n_partition_dates(self, n_partitions, to_date):

        root_path = self.path.replace("/date={date}", "")
        part_list = list(
            filter(
                lambda x: x.split("/")[-1] != "_SUCCESS" and datetime.strptime(x.split("=")[-1], "%Y-%m-%d") <= to_date,
                self.fs.listdir(root_path, detail=False),
            )
        )[-n_partitions:]
        date_list = [datetime.strptime(x.split("=")[-1], self.date_format) for x in part_list]
        return date_list

    def load(
        self,
        polars: bool,
        load_args: Dict[str, Any],
        keys: Optional[Union[pl.DataFrame, pd.DataFrame]] = None,
    ) -> Union[pl.DataFrame, pd.DataFrame]:
        self._check_load_args(load_args=load_args)

        from_date: datetime = load_args["from_date"]
        to_date: datetime = load_args["to_date"]

        columns_arg = None
        if "columns" in load_args and isinstance(load_args["columns"], Mapping):
            load_args = deepcopy(load_args)
            columns_arg = load_args["columns"]
            load_args["columns"] = list(columns_arg.keys())

        n_partitions: Optional[int] = load_args.get("n_partitions")
        date_list = (
            self.get_last_n_partition_dates(n_partitions=n_partitions, to_date=to_date)
            if n_partitions
            else pd.date_range(start=from_date, end=to_date)
        )

        filter_args = self.__load_args__ + self.__extra_args__
        load_args = {key: value for key, value in load_args.items() if key not in filter_args}

        dfs = []
        for date in date_list:
            load_path = self.get_path(date=date)
            data = load_parquet(fs=self.fs, path=load_path, polars=polars, **load_args)
            if polars:
                data = cast(pl.DataFrame, data)
                data = data.with_columns([pl.lit(date.date()).alias("date")])
                if columns_arg is not None:
                    data = data.select([pl.col(col).cast(dtype) for col, dtype in columns_arg.items()])
                if keys is not None:
                    keys = cast(pl.DataFrame, keys)
                    keys_subset = keys.filter(pl.col("date").cast(pl.Date) == date.date()).drop("date")
                    data = data.join(keys_subset, on=keys_subset.columns, how="inner")  # type: ignore
            else:
                data = cast(pd.DataFrame, data)
                data["date"] = date.date()
                if columns_arg is not None:
                    data = data.astype(columns_arg)
                if keys is not None:
                    keys = cast(pd.DataFrame, keys)
                    keys_subset = keys[keys["date"].dt.date == date.date()].drop("date", axis=1)
                    data = data.merge(keys_subset, on=keys_subset.columns.tolist(), how="inner")  # type: ignore

            if "frac" in load_args:
                data = data.sample(frac=load_args["frac"])
            dfs.append(data)

        final_df = pl.concat(dfs) if polars else pd.concat(dfs)
        return final_df
