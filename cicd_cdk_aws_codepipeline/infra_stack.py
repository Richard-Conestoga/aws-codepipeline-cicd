from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class Rb8903530InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "Rb8903530ArtifactsBucket",
            bucket_name="rb8903530-artifacts-bucket",
            versioned=True,
        )

        table = dynamodb.Table(
            self,
            "Rb8903530Table",
            table_name="rb8903530-items-table",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        lambda_fn = _lambda.Function(
            self,
            "Rb8903530Lambda",
            function_name="rb8903530-handler-fn",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
            environment={
                "TABLE_NAME": table.table_name,
                "BUCKET_NAME": bucket.bucket_name,
                "APP_VERSION": "rb8903530-v1",
            },
        )

        table.grant_read_write_data(lambda_fn)
        bucket.grant_read_write(lambda_fn)
