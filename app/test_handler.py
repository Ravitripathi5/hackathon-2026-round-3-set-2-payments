import os
import unittest
from unittest import mock

os.environ["TABLE_NAME"] = "h3-p01-payments"
os.environ["APP_VERSION"] = "v1"

import handler  # noqa: E402


class FakeClientError(Exception):
    pass


class PaymentsTests(unittest.TestCase):
    def test_idempotent_put(self):
        with mock.patch.object(handler, "table") as tbl:
            tbl.return_value.put_item.return_value = {}
            event = {"Records": [{"messageId": "1", "body": '{"payment_id":"p1","amount":5}'}]}
            res = handler.lambda_handler(event, None)
        self.assertEqual(res["batchItemFailures"], [])
        kwargs = tbl.return_value.put_item.call_args.kwargs
        self.assertIn("attribute_not_exists", kwargs["ConditionExpression"])

    def test_duplicate_is_success(self):
        err = type("ConditionalCheckFailedException", (Exception,), {})()
        with mock.patch.object(handler, "table") as tbl:
            tbl.return_value.put_item.side_effect = err
            event = {"Records": [{"messageId": "1", "body": '{"payment_id":"p1","amount":5}'}]}
            res = handler.lambda_handler(event, None)
        self.assertEqual(res["batchItemFailures"], [])

    def test_partial_failure(self):
        with mock.patch.object(handler, "table") as tbl:
            tbl.return_value.put_item.side_effect = RuntimeError("boom")
            event = {"Records": [{"messageId": "bad", "body": '{"payment_id":"p1","amount":5}'}]}
            res = handler.lambda_handler(event, None)
        self.assertEqual(res["batchItemFailures"], [{"itemIdentifier": "bad"}])


if __name__ == "__main__":
    unittest.main()
