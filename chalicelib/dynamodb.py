import boto3

_dynamodb_client = boto3.client("dynamodb")


def get_item(table_name: str, key: dict) -> dict:
    return _dynamodb_client.get_item(TableName=table_name, Key=key)


def put_item(table_name: str, item: str) -> dict:
    return _dynamodb_client.put_item(TableName=table_name, Item=item)
