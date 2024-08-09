resource "aws_cloudwatch_event_rule" "health" {
  name        = "${var.name_prefix}capture-health-events"
  description = "Captures PHD events"

  event_pattern = jsonencode({
    detail-type = ["AWS Health Event"]
    source      = ["aws.health"]
  })
}

resource "aws_cloudwatch_event_target" "health" {
  arn       = aws_sns_topic.account_alerts.arn
  rule      = aws_cloudwatch_event_rule.health.name
  target_id = "SendToSNS-health"
}
