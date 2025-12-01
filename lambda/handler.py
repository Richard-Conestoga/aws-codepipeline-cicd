import os
import json

TABLE_NAME = os.environ.get("TABLE_NAME")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


def main(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Hello from Lambda via CI/CD!",
                "table": TABLE_NAME,
                "bucket": BUCKET_NAME,
            }
        ),
    }
