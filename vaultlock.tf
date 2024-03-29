resource "aws_cloudwatch_event_rule" "glacier_vaultlock" {
  name        = "glacier-vaultlock-monitor"
  description = "Capture glacier vault lock rules"

  event_pattern = jsonencode({
    source      = ["aws.glacier"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventSource = ["glacier.amazonaws.com"]
      eventName = [
        "AbortVaultLock",
        "CompleteVaultLock",
        "DeleteVaultAccessPolicy",
        "InitiateVaultLock",
        "SetVaultAccessPolicy"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "glacier_vaultlock" {
  rule      = aws_cloudwatch_event_rule.glacier_vaultlock.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.account_alerts.arn
}

resource "aws_cloudwatch_event_rule" "backup_vaultlock" {
  name = "backup-vaultlock-monitor"

  event_pattern = jsonencode({
    source      = ["aws.backup"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventSource = ["backup.amazonaws.com"]
      eventName = [
        "AbortVaultLock",
        "DeleteBackupVaultLockConfiguration",
        "StartBackupVaultLock"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "backup_vaultlock" {
  rule      = aws_cloudwatch_event_rule.backup_vaultlock.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.account_alerts.arn
}
