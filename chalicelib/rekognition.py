import boto3

_rekognition_client = boto3.client("rekognition")


def detect_labels(bucket: str, key: str) -> dict:
    return _rekognition_client.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}
    )
