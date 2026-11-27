# 09: AWS Serverless API (API Gateway, Lambda, DynamoDB)

## Objective
Deploy a small HTTP API using API Gateway HTTP API, Python 3.12 Lambda and DynamoDB on-demand storage. Lambda runs in two private subnets with DynamoDB, CloudWatch Logs and X-Ray VPC endpoints and no NAT Gateway. The stack includes KMS encryption, VPC Flow Logs, active X-Ray tracing, reserved concurrency, an encrypted SQS dead-letter queue, a Lambda code-signing configuration and API access logging. The API route requires AWS IAM authorization.

## API
- `GET /` returns a health response.
- `POST /` validates a JSON `message` and writes an item to DynamoDB.
- Both routes require AWS IAM authorization; clients must sign requests with AWS Signature Version 4.
- Unsupported methods return 405; malformed/empty payloads return 400.

## Local tests
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

The unit tests mock DynamoDB and do not require AWS credentials.

## Terraform
```bash
cd terraform
terraform init
terraform fmt -check
terraform validate
terraform plan
```

Review the plan and costs before any apply. DynamoDB uses on-demand billing, point-in-time recovery and server-side encryption. KMS keys, CloudWatch log ingestion/retention, Lambda, API Gateway, Flow Logs and other provisioned services may incur charges. The DynamoDB gateway endpoint does not incur an hourly endpoint charge. CloudWatch Logs and X-Ray interface endpoints are billed hourly and by data processed. The private VPC and DynamoDB gateway endpoint are included; no NAT Gateway is created. No resources are created by CI.

## Security and operational notes
- Lambda uses private subnets and a DynamoDB gateway endpoint. It also uses private CloudWatch Logs and X-Ray interface endpoints with private DNS. The Lambda security group allows TCP/443 to the DynamoDB prefix list and within the VPC CIDR; the interface endpoint security group accepts HTTPS only from the Lambda security group. The execution role includes the X-Ray write actions required for active tracing.
- The Lambda signing configuration is set to `Warn` so the unsigned local ZIP can be used in a lab. Production must switch to `Enforce` and sign the artifact in a trusted release pipeline.
- The SQS DLQ is for asynchronous Lambda invocations. API Gateway invokes this function synchronously, so synchronous request failures still require API/client error handling and observability.
- KMS encryption is enabled for Lambda environment variables, Lambda logs, API access logs and VPC Flow Logs; DynamoDB and SQS use their configured server-side encryption.
- X-Ray tracing is active and Lambda reserved concurrency is capped to five executions.
- Add API throttling, request size limits, alarms and WAF before production.
- Use workload identity/OIDC for CI deployment; never store long-lived AWS keys in Git.
- The example archive contains only the Lambda source file; package dependencies into the deployment artifact if adding non-runtime dependencies.

## Validation boundary
The Python handler is unit-tested with a mocked DynamoDB table. Terraform formatting, provider initialization, plan and live API tests require the corresponding CI tools and an AWS test account. No cloud deployment is performed automatically.
