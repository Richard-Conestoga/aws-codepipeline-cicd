from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class CicdCdkAwsCodepipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket to store static files or artifacts
        bucket = s3.Bucket(self, "LabBucket")

        # DynamoDB table for basic CRUD operations
        table = dynamodb.Table(
            self,
            "LabTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
        )

        # Lambda function
        function = _lambda.Function(
            self,
            "LabFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name,
                "BUCKET_NAME": bucket.bucket_name,
            },
        )

        # Permissions for Lambda
        table.grant_read_write_data(function)
        bucket.grant_read_write(function)
