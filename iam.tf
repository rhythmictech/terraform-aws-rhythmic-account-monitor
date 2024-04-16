resource "aws_accessanalyzer_analyzer" "analyzer" {
  count = var.enable_iam_access_analyzer ? 1 : 0

  analyzer_name = "${var.name_prefix}default-access-analyzer"
  type          = "ACCOUNT"
  tags          = local.tags
}

resource "aws_accessanalyzer_analyzer" "analyzer_unused" {
  count = var.enable_iam_access_analyzer ? 1 : 0

  analyzer_name = "${var.name_prefix}default-unused-access-analyzer"
  type          = "ACCOUNT_UNUSED_ACCESS"
  tags          = local.tags

  configuration {
    unused_access {
      unused_access_age = var.iam_analyzer_unused_access_age
    }
  }
}

resource "aws_cloudwatch_event_rule" "analyzer" {
  count = var.enable_iam_access_analyzer ? 1 : 0

  name_prefix = substr("iam-aa-finding-rhythmic", 0, 35)
  description = "Match on IAM Access Analyzer finding (Rhythmic)"

  event_pattern = <<EOT
{
  "detail-type": [
    "Access Analyzer Finding"
  ],
  "source": [
    "aws.access-analyzer"
  ]
}
EOT
}

resource "aws_cloudwatch_event_target" "analyzer" {
  count = var.enable_iam_access_analyzer ? 1 : 0

  arn       = aws_sns_topic.account_alerts.arn
  rule      = aws_cloudwatch_event_rule.analyzer[0].name
  target_id = "send-to-rhythmic"
}
