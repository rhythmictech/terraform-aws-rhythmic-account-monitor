resource "aws_cloudwatch_event_rule" "backup" {

  name        = "${var.name_prefix}backup-events-monitor"
  description = "Capture AWS Backup events"

  event_pattern = jsonencode({
    source      = ["aws.backup"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventSource = ["backup.amazonaws.com"]
      eventName = [
        "DeleteBackupPlan",
        "DeleteBackupSelection",
        "DeleteBackupVault",
        "DeleteRecoveryPoint",
        "PutBackupVaultAccessPolicy",
        "UpdateRecoveryPointLifecycle"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "backup" {
  arn       = aws_sns_topic.account_alerts.arn
  rule      = aws_cloudwatch_event_rule.backup.name
  target_id = "SendToSNS"
}

# TODO only include negative backup events for now until the datadog terraform
# provider adds support for event pipelines
resource "aws_cloudwatch_event_rule" "backup_event" {

  name_prefix = "backup-events-monitor"
  description = "AWS Backup failures"

  event_pattern = <<EOT
{
  "source": ["aws.backup"],
  "detail-type": ["Backup Job State Change"],
  "detail": {
    "state": ["EXPIRED", "FAILED", "ABORTED"]
  }
}
EOT
}

resource "aws_cloudwatch_event_target" "backup_event" {
  arn       = aws_sns_topic.account_alerts.arn
  rule      = aws_cloudwatch_event_rule.backup_event.name
  target_id = "SendToSNS"
}
