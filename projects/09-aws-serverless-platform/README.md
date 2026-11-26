# 09 — AWS Serverless API (API Gateway, Lambda, DynamoDB)

## Objective
Deploy a small HTTP API using API Gateway HTTP API, Python 3.12 Lambda and DynamoDB on-demand storage. The Lambda role is scoped to write only to the project table and send failed asynchronous invocations to an encrypted SQS dead-letter queue. The API route uses AWS IAM authorization, and the HTTP API stage sends structured access logs to a retained CloudWatch log group. A Lambda code-signing configuration is attached.

## API
- `GET /` returns a health response.
- `POST /` validates a JSON `message` and writes an item to DynamoDB.
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
Review the plan and costs before any apply. The DynamoDB table uses on-demand billing, point-in-time recovery and server-side encryption. API Gateway and Lambda usage may incur charges. No resources are created by CI.

## Security and operational notes
- The Lambda signing configuration is set to `Warn` so the unsigned local ZIP can be deployed in a lab. Production must switch to `Enforce` and sign the artifact in a trusted build pipeline before deployment.\n- The SQS DLQ is configured for asynchronous Lambda invocations; API Gateway invokes this function synchronously, so synchronous request failures still need API-level retry/error handling and client-side observability.\n- The Lambda code-signing policy uses `Warn` so the example unsigned ZIP can be deployed in a lab. For production, switch to `Enforce` and sign the deployment artifact in a trusted release pipeline.\n- The SQS DLQ applies to asynchronous Lambda invocations. API Gateway invokes this function synchronously, so client/API error handling is still required for synchronous failures.\n- Use workload identity/OIDC for CI deployment; never store long-lived AWS keys in Git.
- Add API throttling, request size limits, alarms and WAF before production. Access logs are enabled by this Terraform configuration.
- Add schema validation and authorization; this demonstration endpoint is not an authenticated public write API.
- Restrict log permissions further to a pre-created log group for a production deployment.
- The example archive contains only the Lambda source file; package dependencies into the deployment artifact if adding non-runtime dependencies.

## Validation boundary
The Python handler is unit-tested with a mocked DynamoDB table. Terraform formatting, provider initialization, plan and live API tests require the corresponding CI tools and an AWS test account. No cloud deployment is performed automatically.
