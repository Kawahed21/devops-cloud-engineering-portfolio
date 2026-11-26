# 09 — AWS Serverless API (API Gateway, Lambda, DynamoDB)

## Objective
Deploy a small HTTP API using API Gateway HTTP API, Python 3.12 Lambda and DynamoDB on-demand storage. The Lambda role is scoped to write only to the project table, with a separate CloudWatch Logs permission statement.

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
- Use workload identity/OIDC for CI deployment; never store long-lived AWS keys in Git.
- Add API throttling, request size limits, structured logs, alarms and WAF before production.
- Add schema validation and authorization; this demonstration endpoint is not an authenticated public write API.
- Restrict log permissions further to a pre-created log group for a production deployment.
- The example archive contains only the Lambda source file; package dependencies into the deployment artifact if adding non-runtime dependencies.

## Validation boundary
The Python handler is unit-tested with a mocked DynamoDB table. Terraform formatting, provider initialization, plan and live API tests require the corresponding CI tools and an AWS test account. No cloud deployment is performed automatically.
