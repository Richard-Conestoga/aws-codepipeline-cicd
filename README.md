# Infrastructure-as-code demo using AWS CDK (Python) with a CI/CD pipeline on AWS CodePipeline and CodeBuild.

## What this project does

This CDK app deploys:

- An S3 bucket (`LabBucket`)
- A DynamoDB table (`LabTable`) with partition key `id`
- A Lambda function (`LabFunction`) that:
  - Reads environment variables `TABLE_NAME` and `BUCKET_NAME`
  - Returns a JSON message including the table and bucket names

The project also has a CI/CD pipeline:

- Source: GitHub (via GitHub App, Pipeline Type V2)
- Build: CodeBuild using `buildspec.yml`
  - Creates a Python virtualenv
  - Installs CDK + dependencies
  - Runs `cdk synth`
  - Runs `cdk deploy --require-approval never`

Pushing to the `main` branch triggers the pipeline automatically.

## Project structure

- `app.py` – CDK app entrypoint
- `cicd_cdk_aws_codepipeline/`
  - `cicd_cdk_aws_codepipeline_stack.py` – defines S3, Lambda, DynamoDB
- `lambda/handler.py` – Lambda function code
- `buildspec.yml` – CodeBuild configuration
- `requirements.txt` – Python dependencies

## Prerequisites

- AWS account and IAM user/role with CDK permissions
- AWS CDK v2 installed (`cdk --version`)
- Node.js (supported LTS version)
- Python 3.12
- Bootstrapped environment:
  - `cdk bootstrap aws://<account-id>/us-east-1`

## Local development

```

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cdk synth
cdk deploy

```

To tear down the stack:

```

cdk destroy

```

## CI/CD pipeline notes

- Uses CodePipeline **V2** with execution mode `superseded`.
- Source: GitHub (via GitHub App) with a push webhook on `main`.
- Build: CodeBuild project configured to “Use a buildspec file”.
- The CodeBuild role needs permissions to:
  - Read SSM parameters for CDK bootstrap version
  - Access the CDK bootstrap S3 bucket
  - `iam:PassRole` for the CDK CloudFormation execution role