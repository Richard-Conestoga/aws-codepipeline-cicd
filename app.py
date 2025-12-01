import aws_cdk as cdk

from cicd_cdk_aws_codepipeline.cicd_cdk_aws_codepipeline_stack import (
    CicdCdkAwsCodepipelineStack,
)

app = cdk.App()
CicdCdkAwsCodepipelineStack(app, "CicdCdkAwsCodepipelineStack")
app.synth()
