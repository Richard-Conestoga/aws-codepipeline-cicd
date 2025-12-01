#!/usr/bin/env python3
import aws_cdk as cdk
from cicd_cdk_aws_codepipeline.infra_stack import Rb8903530InfraStack
from cicd_cdk_aws_codepipeline.pipeline_stack import Rb8903530PipelineStack

app = cdk.App()

infra = Rb8903530InfraStack(app, "Rb8903530InfraStack")

Rb8903530PipelineStack(
    app,
    "Rb8903530PipelineStack",
    repo_owner="Richard-Conestoga",
    repo_name="aws-codepipeline-cicd",
    branch="main",
    connection_arn="arn:aws:codestar-connections:us-east-1:349070XXXXXX:connection/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
)

app.synth()
