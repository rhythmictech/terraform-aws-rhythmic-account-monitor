resource "aws_cloudwatch_event_rule" "organizations" {
  name        = "${var.name_prefix}capture-organizations-account-changes"
  description = "Captures Organizations API calls related to account lifecycle and configuration"

  event_pattern = jsonencode({
    source = ["aws.organizations"]
    detail = {
      eventName = [
        "CloseAccount",
        "CreateAccount",
        "CreateGovCloudAccount",
        "DeleteAccount",
        "InviteAccountToOrganization",
        "LeaveOrganization",
        "ListAccounts", # for testing purpose to generate noise
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
  target_id = "SendToSNS-organizations"
}

resource "aws_cloudwatch_event_rule" "control_tower" {
  name        = "${var.name_prefix}capture-organizations-account-changes"
  description = "Captures Control Tower API calls related to account lifecycle and configuration"

  event_pattern = jsonencode({
    source = ["aws.controltower"]
    detail = {
      eventName = ["CreateManagedAccount", "UpdateManagedAccount"]
    }
  })
}

resource "aws_cloudwatch_event_target" "control_tower" {
  arn       = aws_sns_topic.account_alerts.arn
  rule      = aws_cloudwatch_event_rule.organizations.name
  target_id = "SendToSNS-controltower"
}
