from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Optional, Union

import pandas as pd
import polars as pl
from loguru import logger
from playground.core.data.dataset_base import Dataset
from playground.core.data.parquet_dataset import DatePartitionedParquetDataset, ParquetDataset
from playground.core.s3_source.ml_lake import s3source_mllake
from playground.core.s3_source.recsys import s3source_recsys
from pyarrow import parquet


class DataCatalog:
    def __init__(
        self,
        datasets: Dict[str, Dict[str, Dataset]],
    ):
        self.datasets = datasets

    def add_dataset(self, layer: str, alias: str, dataset: Dataset) -> None:
        if layer in self.datasets:
            if alias in self.datasets[layer]:
                logger.info(
                    f"dataset {alias} is already present in the catalog layers {layer},"
                    " replacing it with the new dataset"
                )
            self.datasets[layer][alias] = dataset
        else:
            self.datasets[layer] = {alias: dataset}

    def load(
        self,
        layer: str,
        alias: str,
        polars: bool,
        load_args: Dict[str, Any],
        keys: Optional[Union[pl.DataFrame, pd.DataFrame]] = None,
    ) -> Union[pl.DataFrame, pd.DataFrame]:
        if alias not in self.datasets[layer]:
            raise ValueError(f"dataset with alias {alias} is not present in the catalog layer {layer}")
        return self.datasets[layer][alias].load(polars=polars, load_args=load_args, keys=keys)

    def get(self, layer: str, alias: str) -> Dataset:
        if layer not in self.datasets:
            raise ValueError(f"unknown layer={layer}")
        if alias not in self.datasets[layer]:
            raise ValueError(f"unknown alias={alias}")
        return self.datasets[layer][alias]

    def describe_ds(self, layer: str, alias: str, date: datetime) -> Dict[str, Any]:
        dataset = CATALOG.get(layer=layer, alias=alias)
        path = dataset.get_path(date=date)
        parq = parquet.ParquetDataset(path, filesystem=dataset.fs)
        nrows = 0
        for piece in parq.pieces:
            nrows += piece.get_metadata().num_rows
        schema = {field.name: field.physical_type for field in parq.schema}
        schema["n_rows"] = nrows
        return schema

    def load_datasets(
        self,
        polars: bool,
        dataset_alias_to_load_config: Dict[str, Dict[str, Any]],
        keys_dict: Optional[Dict[str, Dict[str, Union[pl.DataFrame, pd.DataFrame]]]] = None,
    ) -> Dict[str, Dict[str, Union[pl.DataFrame, pd.DataFrame]]]:

        missing_aliases = defaultdict(list)
        for layer in dataset_alias_to_load_config:
            if layer not in self.datasets:
                for alias in dataset_alias_to_load_config[layer]:
                    missing_aliases[layer].append(alias)
            else:
                for alias in dataset_alias_to_load_config[layer]:
                    if alias not in self.datasets[layer]:
                        missing_aliases[layer].append(alias)

        if missing_aliases:
            raise ValueError(f"datasets {missing_aliases} are not present in the catalog")

        result: Dict[str, Dict[str, Union[pl.DataFrame, pd.DataFrame]]] = defaultdict(dict)
        for layer in dataset_alias_to_load_config:
            for alias, load_args in dataset_alias_to_load_config[layer].items():
                logger.info(f"Loading {alias} dataset from the layer {layer}")
                if keys_dict is None:
                    result[layer][alias] = self.load(layer=layer, alias=alias, polars=polars, load_args=load_args)
                else:
                    result[layer][alias] = self.load(
                        layer=layer,
                        alias=alias,
                        polars=polars,
                        load_args=load_args,
                        keys=keys_dict.get(layer, {}).get(alias),
                    )
        return result


CATALOG = DataCatalog(
    datasets={
        "raw": {
            "line_items": DatePartitionedParquetDataset(
                path="data/raw/instamart_db/line_items_completed", source=s3source_mllake
            ),
            "registered_users": ParquetDataset(path="data/raw/instamart_db/registered_users", source=s3source_mllake),
            "products": ParquetDataset(path="data/raw/instamart_db/products", source=s3source_mllake),
            "prices": ParquetDataset(path="data/raw/instamart_db/prices", source=s3source_mllake),
            "favorite_products": ParquetDataset(path="data/raw/instamart_db/favorite_products", source=s3source_mllake),
            "shipments": DatePartitionedParquetDataset(path="data/raw/analytics_db/shipments", source=s3source_mllake),
            "alcohol": ParquetDataset(path="data/raw/instamart_db/alcohol", source=s3source_mllake),
            "master_categories": ParquetDataset(path="data/raw/instamart_db/master_categories", source=s3source_mllake),
            "retailers": ParquetDataset(path="data/raw/instamart_db/retailers", source=s3source_mllake),
            "stores": ParquetDataset(path="data/raw/instamart_db/stores", source=s3source_mllake),
        },
        "agg": {
            "anonymous_user_unique_mapping": ParquetDataset(
                path="data/agg/user_mappings/anonymous_user_unique_mapping", source=s3source_mllake
            ),
            "user_product_interaction": DatePartitionedParquetDataset(
                path="data/agg/user_product/user_product_interaction", source=s3source_mllake
            ),
        },
        "feat": {
            "fasttext_products": ParquetDataset(path="data/feat/product/embedding_fasttext", source=s3source_mllake),
            "sbert_products": ParquetDataset(path="data/feat/product/embedding_bert", source=s3source_mllake),
            "product_price": DatePartitionedParquetDataset(
                path="data/feat/product/price",
                source=s3source_mllake,
                key=["date", "store_id", "product_sku"],
            ),
            "product_order_stats": DatePartitionedParquetDataset(
                path="data/feat/product/order_stats",
                source=s3source_mllake,
                key=["date", "product_sku"],
            ),
            "product_retailer_order": DatePartitionedParquetDataset(
                path="data/feat/product/retailer_order",
                source=s3source_mllake,
                key=["date", "retailer_id", "product_sku"],
            ),
            "product_brands": DatePartitionedParquetDataset(
                path="data/feat/product/brands",
                source=s3source_mllake,
                key=["date", "product_sku"],
            ),
            "retailer_order_stats": DatePartitionedParquetDataset(
                path="data/feat/retailer/order_stats",
                source=s3source_mllake,
                key=["date", "retailer_id"],
            ),
            "user_discount": DatePartitionedParquetDataset(
                path="data/feat/user/discount",
                source=s3source_mllake,
                key=["date", "user_id"],
            ),
            "user_discount_sku": DatePartitionedParquetDataset(
                path="data/feat/user/discount_sku",
                source=s3source_mllake,
                key=["date", "user_id", "product_sku"],
            ),
            "user_order_sku_stats": DatePartitionedParquetDataset(
                path="data/feat/user/order_sku_stats",
                source=s3source_mllake,
                key=["date", "user_id", "product_sku"],
            ),
            "user_product_counts": DatePartitionedParquetDataset(
                path="data/feat/user_product/counts",
                source=s3source_mllake,
                key=["date", "user_id", "product_sku"],
            ),
            "user_product_recency": DatePartitionedParquetDataset(
                path="data/feat/user_product/recency",
                source=s3source_mllake,
                key=["date", "user_id", "product_sku"],
            ),
            "user_relevance": DatePartitionedParquetDataset(
                path="data/feat/user/user_relevance",
                source=s3source_mllake,
                key=["date", "user_id", "brand_id"],
            ),
            "user_category_relevance": DatePartitionedParquetDataset(
                path="data/feat/user/user_category_relevance",
                source=s3source_mllake,
                key=["date", "user_id", "master_category_id", "brand_id"],
            ),
            "user_order_stats": DatePartitionedParquetDataset(
                path="data/feat/user/order_stats",
                source=s3source_mllake,
                key=["date", "user_id"],
            ),
            "user_store_stats_ctr": DatePartitionedParquetDataset(
                path="data/feat/user_store/user_store_stats_ctr",
                source=s3source_mllake,
                key=["date", "user_id", "store_id"],
            ),
            "store_stats_ctr": DatePartitionedParquetDataset(
                path="data/feat/store/store_stats_ctr",
                source=s3source_mllake,
                key=["date", "store_id"],
            ),
            "store_stats_aov": DatePartitionedParquetDataset(
                path="data/feat/store/store_stats_aov",
                source=s3source_mllake,
                key=["date", "store_id"],
            ),
        },
        "recsys": {
            "parrots": ParquetDataset(
                path="recsys_2.0/prod/experiment/parrots/recsys_validation_dataset", source=s3source_recsys
            ),
        },
    }
)
