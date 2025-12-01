import os
import json
import boto3

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]


def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    item = {
        "id": "test-" + (getattr(context, "aws_request_id", "local")),
        "message": "hello from rb8903530",
    }

    table.put_item(Item=item)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="rb8903530-test-object.json",
        Body=json.dumps(item).encode("utf-8"),
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"ok": True, "item": item}),
    }
