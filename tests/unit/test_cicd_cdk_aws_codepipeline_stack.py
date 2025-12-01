import aws_cdk as core
import aws_cdk.assertions as assertions

from cicd_cdk_aws_codepipeline.pipeline_stack import CicdCdkAwsCodepipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cicd_cdk_aws_codepipeline/cicd_cdk_aws_codepipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CicdCdkAwsCodepipelineStack(app, "cicd-cdk-aws-codepipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
