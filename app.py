#!/usr/bin/env python3
import aws_cdk as cdk
# from cicd_cdk_aws_codepipeline.infra_stack import Rb8903530InfraStack
from cicd_cdk_aws_codepipeline.pipeline_stack import Rb8903530PipelineStack

app = cdk.App()

# Optional direct deploy of infra stack
# Rb8903530InfraStack(app, "Rb8903530InfraStack")

Rb8903530PipelineStack(
    app,
    "Rb8903530PipelineStack",
    repo_owner="Richard-Conestoga",
    repo_name="aws-codepipeline-cicd",
    branch="main",
    connection_arn="arn:aws:codeconnections:us-east-1:349070093011:connection/fe767164-5b41-43b1-98c5-6d9fee3d6cda",
)

app.synth()
