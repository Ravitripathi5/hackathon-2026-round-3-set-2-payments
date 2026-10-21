"""FIFO Payment Worker - idempotent DynamoDB writes with partial batch failures."""
import json
import os

TABLE_NAME = os.environ.get("TABLE_NAME", "")
APP_VERSION = os.environ.get("APP_VERSION", "dev")

_table = None


def table():
    global _table
    if _table is None:
        import boto3
        _table = boto3.resource("dynamodb").Table(TABLE_NAME)
    return _table


def process_record(record):
    body = json.loads(record.get("body") or "{}")
    payment_id = str(body.get("payment_id") or "").strip()
    amount = body.get("amount")
    if not payment_id:
        raise ValueError("payment_id required")
    try:
        table().put_item(
            Item={
                "payment_id": payment_id,
                "amount": str(amount),
                "version": APP_VERSION,
            },
            ConditionExpression="attribute_not_exists(payment_id)",
        )
    except Exception as exc:  # noqa: BLE001
        # ConditionalCheckFailedException means already processed — treat as success.
        name = type(exc).__name__
        if "ConditionalCheckFailed" in name or "ConditionalCheckFailedException" in str(exc):
            return
        raise


def lambda_handler(event, context):
    failures = []
    for record in event.get("Records") or []:
        try:
            process_record(record)
        except Exception:  # noqa: BLE001
            failures.append({"itemIdentifier": record.get("messageId")})
    return {"batchItemFailures": failures}
