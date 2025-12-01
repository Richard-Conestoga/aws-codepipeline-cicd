from aws_cdk import Stack
from aws_cdk import pipelines
from constructs import Construct

from cicd_cdk_aws_codepipeline.cicd_cdk_aws_codepipeline_stack import (
    CicdCdkAwsCodepipelineStack,
)


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, connection_arn: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Source from GitHub via CodeStar Connection
        source = pipelines.CodePipelineSource.connection(
            "Richard-Conestoga/aws-codepipeline-cicd",  # owner/repo
            "main",
            connection_arn=connection_arn,
        )

        synth = pipelines.ShellStep(
            "Synth",
            input=source,
            commands=[
                "npm install -g aws-cdk",
                "python -m venv .venv",
                "source .venv/bin/activate",
                "pip install -r requirements.txt",
                "cdk synth",
            ],
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=synth,
        )

        # Add our application stack as a stage
        pipeline.add_stage(
            pipelines.CodePipelineStep(
                "DeployApp",
                stack=CicdCdkAwsCodepipelineStack(self, "AppStack"),
            )
        )
