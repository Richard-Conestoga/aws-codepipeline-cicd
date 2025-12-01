from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
)
from constructs import Construct


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

        source_output = codepipeline.Artifact()

        pipeline = codepipeline.Pipeline(
            self,
            "Rb8903530Pipeline",
            pipeline_name="rb8903530-cdk-pipeline",
        )

        pipeline.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess")
        )

        source_action = cp_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub_Source",
            owner=repo_owner,
            repo=repo_name,
            branch=branch,
            connection_arn=connection_arn,
            output=source_output,
        )

        pipeline.add_stage(
            stage_name="Source",
            actions=[source_action],
        )

        codebuild_role = iam.Role(
            self,
            "Rb8903530CodeBuildRole",
            role_name="rb8903530-codebuild-role",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
        )

        codebuild_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        project = codebuild.PipelineProject(
            self,
            "Rb8903530CodeBuild",
            project_name="rb8903530-cdk-build",
            role=codebuild_role,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
            ),
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "install": {
                            "commands": [
                                "python -m pip install --upgrade pip",
                                "pip install -r requirements.txt",
                                "npm install -g aws-cdk",
                            ]
                        },
                        "build": {
                            "commands": [
                                "cdk synth",
                                "cdk deploy Rb8903530InfraStack --require-approval never",
                            ]
                        },
                    },
                }
            ),
        )

        build_action = cp_actions.CodeBuildAction(
            action_name="CDK_Build_Deploy",
            project=project,
            input=source_output,
        )

        pipeline.add_stage(
            stage_name="BuildAndDeploy",
            actions=[build_action],
        )
