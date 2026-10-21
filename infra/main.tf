# Set 2 - FIFO Payment Worker.
#
# TODO ECR ${local.prefix}-payments (IMMUTABLE, scan on push)
# TODO SQS FIFO ${local.prefix}-payments.fifo (content-based dedup) + DLQ ${local.prefix}-payments-dlq.fifo maxReceiveCount 3
# TODO DynamoDB ${local.prefix}-payments (pk payment_id)
# TODO IAM role ${local.prefix}-payments-role + boundary
# TODO Lambda ${local.prefix}-payments Image arm64 + event source mapping
# TODO Log group retention 14
