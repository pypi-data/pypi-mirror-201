from playground.core.s3_source.base import S3Source

s3source_recsys = S3Source(
    aws_access_key="RECSYS_AWS_ACCESS_KEY",
    aws_secret_key="RECSYS_AWS_SECRET_KEY",
    bucket="RECSYS_BUCKET",
)
