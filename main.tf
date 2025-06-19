data "aws_caller_identity" "current" {
}

data "aws_region" "current" {
}

data "aws_partition" "current" {
}

module "tags" {
  source  = "rhythmictech/tags/terraform"
  version = "~> 1.1.1"

  enforce_case = "UPPER"
  names        = ["Rhythmic-AccountMonitoring"]
  tags = merge(var.tags, {
    "team"    = "Rhythmic"
    "service" = "aws_managed_services"
    "env"     = "ops"
  })
}

locals {
  account_id = data.aws_caller_identity.current.account_id
  partition  = data.aws_partition.current.partition
  region     = data.aws_region.current.name
  tags       = module.tags.tags_no_name
}

data "aws_kms_alias" "notifications" {
  name = "alias/rhythmic-notifications"
}

resource "aws_sns_topic" "account_alerts" {
  name              = "${var.name_prefix}AccountAlerts"
  kms_master_key_id = "alias/rhythmic-notifications"
  tags              = local.tags
}

data "aws_iam_policy_document" "account_alerts" {
  statement {
    actions = [
      "sns:Publish"
    ]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    resources = [
      aws_sns_topic.account_alerts.arn
    ]
  }
}

resource "aws_sns_topic_policy" "account_alerts" {
  arn    = aws_sns_topic.account_alerts.arn
  policy = data.aws_iam_policy_document.account_alerts.json
}

data "aws_secretsmanager_secret" "datadog_api_key" {
  name = var.datadog_api_key_secret_arn
}

data "aws_secretsmanager_secret_version" "datadog_api_key" {
  secret_id = data.aws_secretsmanager_secret.datadog_api_key.id
}

resource "aws_sns_topic_subscription" "account_alerts" {
  topic_arn = aws_sns_topic.account_alerts.arn
  protocol  = "https"
  endpoint  = "https://app.datadoghq.com/intake/webhook/sns?api_key=${data.aws_secretsmanager_secret_version.datadog_api_key.secret_string}"
}
