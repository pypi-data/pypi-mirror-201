from playground.core.s3_source.base import S3Source

s3source_mllake = S3Source(
    aws_access_key="MLLAKE_AWS_ACCESS_KEY",
    aws_secret_key="MLLAKE_AWS_SECRET_KEY",
    bucket="MLLAKE_BUCKET",
)
