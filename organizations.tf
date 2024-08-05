resource "aws_cloudwatch_event_rule" "organizations" {
  name        = "capture-organizations-account-changes"
  description = "Captures Organizations API calls related to account lifecycle and configuration"

  event_pattern = jsonencode({
    source      = ["aws.organizations"]
    detail-type = ["AWS API Call via CloudTrail"]
    detail = {
      eventSource = ["organizations.amazonaws.com"]
      eventName = [
        "CloseAccount",
        "CreateAccount",
        "CreateGovCloudAccount",
        "DeleteAccount",
        "InviteAccountToOrganization",
        "LeaveOrganization",
        "RemoveAccountFromOrganization",
        "UpdatePolicy",
        "AttachPolicy",
        "DetachPolicy",
        "EnablePolicyType",
        "DisablePolicyType",
        "MoveAccount",
        "TagResource",
        "UntagResource"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "organizations" {
  arn       = aws_sns_topic.account_alerts.arn
  rule      = aws_cloudwatch_event_rule.organizations.name
  target_id = "SendToSNS"
}
