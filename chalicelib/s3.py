import boto3
from botocore.errorfactory import ClientError

_s3_client = boto3.client("s3")


def upload_file_bytes(file_bytes, bucket, key, **kwargs):
    return _s3_client.put_object(Bucket=bucket, Body=file_bytes, Key=key, **kwargs)


def key_exists(bucket: str, key: str) -> bool:
    try:
        _s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def get_object(bucket: str, key: str, **kwargs):
    return _s3_client.get_object(Bucket=bucket, Key=key, **kwargs)
