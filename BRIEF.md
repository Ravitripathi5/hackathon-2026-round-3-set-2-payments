# Set 2 - FIFO Payment Worker

**Scenario.** Checkout emits payment events onto an SQS FIFO queue. A Lambda worker must write each `payment_id` to DynamoDB exactly once (conditional put) and report partial batch failures. Ship the service; review `crack-files/` for a "payment relay" PR.

`<id>` is your participant ID (example `p07`).

## Part A - Build and deploy (50 points)

| What | Exact name or setting |
|---|---|
| ECR | `h3-<id>-payments`, scan on push **on**, tag mutability **IMMUTABLE** |
| Image | `h3-<id>-payments:v1`, Lambda Python 3.12, arm64, `APP_VERSION=v1` |
| SQS FIFO | `h3-<id>-payments.fifo`, content-based deduplication **true** |
| DLQ FIFO | `h3-<id>-payments-dlq.fifo`, redrive `maxReceiveCount = 3`, SSE on both |
| DynamoDB | `h3-<id>-payments`, partition key `payment_id` (S), on-demand |
| Role | `h3-<id>-payments-role` with `permissions_boundary = var.permissions_boundary_arn` |
| Lambda | `h3-<id>-payments`, Image, arm64, env `TABLE_NAME` and `APP_VERSION` |
| Event source | FIFO queue to Lambda, Enabled, partial batch response enabled |
| Logs | `/aws/lambda/h3-<id>-payments`, retention 14 |

**Tasks**
1. **A1 Package (8).** Root Lambda Python 3.12 Dockerfile, `handler.lambda_handler`, arm64 image, `APP_VERSION=v1`; supplied unit tests pass.
2. **A2 Registry (6).** Correct ECR settings and image `:v1`.
3. **A3 IaC (8).** Terraform fmt/validate, no hardcoded account or credentials, and the required role boundary.
4. **A4 Working deployment (17).** Active image Lambda and Enabled event source. Sending one `payment_id` twice with different deduplication IDs preserves the first DynamoDB write. FIFO/content deduplication are configured.
5. **A5 Hardening (6).** DLQ redrive after 3 receives, encryption on both queues, log retention 14.
6. **A6 CI (5).** Root `deploy.yml`: tests, OIDC, ECR build/push, Terraform fmt/validate/plan, no static AWS keys.

Run `python3 tools/check_build.py --id <id>` after deployment.

## Part B / C / Submit
Fix six issues in `crack-files/`, fill `FINDINGS.md`, submit with `tools/submit.py`. Do not destroy resources.
