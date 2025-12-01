from aws_cdk import Stack, Stage
from aws_cdk import pipelines
from constructs import Construct

from cicd_cdk_aws_codepipeline.infra_stack import Rb8903530InfraStack

class Rb8903530AppStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        Rb8903530InfraStack(self, "Rb8903530InfraStack")

class Rb8903530PipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        repo_owner: str,
        repo_name: str,
        branch: str,
        connection_arn: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self,
            "Rb8903530CdkPipeline",
            pipeline_name="rb8903530-cdk-pipeline",
            synth=pipelines.CodeBuildStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    repo_string=f"{repo_owner}/{repo_name}",
                    branch=branch,
                    connection_arn=connection_arn,
                ),
                install_commands=[
                    "python -m pip install --upgrade pip",
                    "pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(Rb8903530AppStage(self, "Rb8903530App"))

