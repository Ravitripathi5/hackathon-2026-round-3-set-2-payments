# Set 2 - FIFO Payment Worker

**Scenario.** Checkout emits payment events onto an SQS FIFO queue. A Lambda worker must write each `payment_id` to DynamoDB exactly once (conditional put) and report partial batch failures. Ship the service; review `crack-files/` for a "payment relay" PR.

`<id>` is your participant ID (example `p07`).

## Part A - Build and deploy (50 points)

| What | Exact name or setting |
|---|---|
| ECR | `h3-<id>-payments`, scan on push, **IMMUTABLE** |
| Image | `h3-<id>-payments:v1` |
| SQS FIFO | `h3-<id>-payments.fifo`, content-based deduplication **true** |
| DLQ FIFO | `h3-<id>-payments-dlq.fifo`, redrive `maxReceiveCount = 3`, SSE on both |
| DynamoDB | `h3-<id>-payments`, partition key `payment_id` (S), on-demand |
| Role | `h3-<id>-payments-role` + permissions boundary |
| Lambda | `h3-<id>-payments`, Image, arm64, event source mapping Enabled |
| Logs | `/aws/lambda/h3-<id>-payments`, retention 14 |

**A4 live check:** send the same payment twice with **different** deduplication ids; exactly **one** DynamoDB item for that `payment_id`.

Package, ECR, Terraform, CI (OIDC), and hardening follow the same Part A structure as other sets (Dockerfile Lambda Python 3.12, `deploy.yml` with tests + OIDC + ECR + terraform fmt/validate/plan).

## Part B / C / Submit
Fix six issues in `crack-files/`, fill `FINDINGS.md`, submit with `tools/submit.py`. Do not destroy resources.
