import os
from typing import Optional

from s3fs import S3FileSystem


def get_s3_storage_options(aws_access_key: Optional[str] = None, aws_secret_key: Optional[str] = None):
    s3_client_params = {"endpoint_url": "https://storage.yandexcloud.net"}
    s3_config_params = {"read_timeout": int(os.environ.get("S3_DELAY", 360))}
    s3_storage_options = {
        "key": aws_access_key or os.getenv("PG_AWS_ACCESS_KEY_ID"),
        "secret": aws_secret_key or os.getenv("PG_AWS_SECRET_ACCESS_KEY"),
        "client_kwargs": s3_client_params,
        "config_kwargs": s3_config_params,
    }

    return s3_storage_options


def get_s3_file_system(aws_access_key: Optional[str] = None, aws_secret_key: Optional[str] = None) -> S3FileSystem:
    s3_storage_options = get_s3_storage_options(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)
    return S3FileSystem(
        anon=False,
        key=s3_storage_options["key"],
        secret=s3_storage_options["secret"],
        client_kwargs=s3_storage_options["client_kwargs"],
    )


class S3Source:
    def __init__(self, aws_access_key: str, aws_secret_key: str, bucket: str):
        self._fs = get_s3_file_system(
            aws_access_key=os.getenv(aws_access_key), aws_secret_key=os.getenv(aws_secret_key)
        )
        self._bucket = os.getenv(bucket)

    @property
    def fs(self) -> S3FileSystem:
        return self._fs

    @property
    def bucket(self) -> str:
        if self._bucket is None:
            raise KeyError("Bucket not exists in enviroment")
        return self._bucket
