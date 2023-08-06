import os
import typing as tp

import s3fs
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem


def get_s3_storage_options(aws_access_key: tp.Optional[str] = None, aws_secret_key: tp.Optional[str] = None):
    s3_key_id = aws_access_key or os.getenv("PG_AWS_ACCESS_KEY_ID")
    s3_key_secret = aws_secret_key or os.getenv("PG_AWS_SECRET_ACCESS_KEY")

    s3_client_params = {"endpoint_url": os.getenv("AWS_ENDPOINT_URL")}
    s3_config_params = {"read_timeout": 3600}
    s3_storage_options = {
        "key": s3_key_id,
        "secret": s3_key_secret,
        "client_kwargs": s3_client_params,
        "config_kwargs": s3_config_params,
    }

    return s3_storage_options


def get_file_system_for_path(
    path: str, aws_access_key: tp.Optional[str] = None, aws_secret_key: tp.Optional[str] = None
) -> AbstractFileSystem:
    if path.startswith("/") and (aws_secret_key or aws_secret_key):
        raise ValueError(f"Received AWS S3 credentials for a local path: {path}")

    if path.startswith("s3://"):
        s3_storage_options = get_s3_storage_options(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)
        return s3fs.S3FileSystem(
            anon=False,
            key=s3_storage_options["key"],
            secret=s3_storage_options["secret"],
            client_kwargs=s3_storage_options["client_kwargs"],
        )
    else:
        return LocalFileSystem(auto_mkdir=True)
