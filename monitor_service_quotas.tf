resource "aws_iam_role" "monitor_service_quotas_execution" {
  name_prefix        = "${var.name_prefix}monitor_service_quotas"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "monitor_service_quotas_execution" {
  statement {
    effect    = "Allow"
    resources = ["*"] #tfsec:ignore:avd-aws-0057

    actions = [
      "service-quotas:ListServices",
      "service-quotas:ListServiceQuotas",
      "service-quotas:GetServiceQuota",
      "service-quotas:GetAWSDefaultServiceQuota"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "ec2:DescribeRegions"
    ]
    resources = ["*"] #tfsec:ignore:avd-aws-0057
  }

  statement {
    effect = "Allow"
    actions = [
      "cloudwatch:GetMetricStatistics",
      "cloudwatch:ListMetrics"
    ]
    resources = ["*"] #tfsec:ignore:avd-aws-0057
  }

  statement {
    effect    = "Allow"
    resources = ["arn:${local.partition}:logs:${local.region}:${local.account_id}:log-group:/aws/lambda/${var.name_prefix}monitor_service_quotas_execution:*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
  }

  statement {
    effect    = "Allow"
    resources = [aws_sns_topic.account_alerts.arn]

    actions = [
      "sns:Publish"
    ]
  }

  statement {
    effect    = "Allow"
    resources = [data.aws_kms_alias.notifications.target_key_arn]

    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey"
    ]
  }
}

resource "aws_iam_policy" "monitor_service_quotas_execution" {
  name_prefix = "${var.name_prefix}monitor_service_quotas_lambda_policy"
  policy      = data.aws_iam_policy_document.monitor_service_quotas_execution.json
}

resource "aws_iam_role_policy_attachment" "monitor_service_quotas_execution" {
  role       = aws_iam_role.monitor_service_quotas_execution.name
  policy_arn = aws_iam_policy.monitor_service_quotas_execution.arn
}

resource "aws_iam_role_policy_attachment" "monitor_service_quotas_security_analyst" {
  role       = aws_iam_role.monitor_service_quotas_execution.name
  policy_arn = "arn:${local.partition}:iam::aws:policy/SecurityAudit"
}

data "archive_file" "monitor_service_quotas" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/monitor_service_quotas"
  output_path = "${path.module}/lambda/monitor_service_quotas.zip"
}

#tfsec:ignore:avd-aws-0066
resource "aws_lambda_function" "monitor_service_quotas" {
  function_name    = "${var.name_prefix}monitor_service_quotas_execution"
  handler          = "lambda.handler"
  role             = aws_iam_role.monitor_service_quotas_execution.arn
  runtime          = "python3.13"
  filename         = data.archive_file.monitor_service_quotas.output_path
  source_code_hash = data.archive_file.monitor_service_quotas.output_base64sha256
  tags             = local.tags
  timeout          = 1020

  environment {
    variables = {
      SNS_TOPIC_ARN             = aws_sns_topic.account_alerts.arn
      SERVICE_QUOTA_THRESHOLD   = var.service_quota_threshold
      SERVICE_QUOTA_REGION_LIST = join(",", var.service_quota_region_list)
    }
  }
}

#tfsec:ignore:avd-aws-0017
resource "aws_cloudwatch_log_group" "monitor_service_quotas" {
  name              = "/aws/lambda/${aws_lambda_function.monitor_service_quotas.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_event_rule" "monitor_service_quotas" {
  name_prefix         = "${var.name_prefix}monitor-ami-usage-trigger"
  description         = "Triggers Lambda at noon ET every day"
  schedule_expression = "cron(0 17 * * ? *)"
}

resource "aws_lambda_permission" "monitor_service_quotas" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monitor_service_quotas.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monitor_service_quotas.arn
}

resource "aws_cloudwatch_event_target" "monitor_service_quotas" {
  rule      = aws_cloudwatch_event_rule.monitor_service_quotas.name
  target_id = "invokeLambdaFunction"
  arn       = aws_lambda_function.monitor_service_quotas.arn
}
