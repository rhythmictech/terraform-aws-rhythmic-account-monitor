data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "monitor_ami_usage_execution" {
  name_prefix        = "Rhythmic-MonitorAMIUsage"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "monitor_ami_usage_execution" {
  statement {
    effect    = "Allow"
    resources = ["*"] #tfsec:ignore:avd-aws-0057

    actions = [
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:DescribeLaunchConfigurations",
      "batch:DescribeComputeEnvironments",
      "cloudformation:DescribeStacks",
      "cloudformation:DescribeStackResources",
      "ec2:DescribeInstances",
      "ec2:DescribeImages",
      "ec2:DescribeLaunchTemplates",
      "ec2:DescribeLaunchTemplateVersions",
      "eks:ListClusters",
      "eks:DescribeNodegroup",
      "eks:ListNodegroups",
      "elasticbeanstalk:DescribeEnvironmentResources",
      "elasticbeanstalk:DescribeEnvironments"
    ]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:logs:${local.region}:${local.account_id}:log-group:/aws/lambda/monitor_ami_usage_execution:*"]

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
}

resource "aws_iam_policy" "monitor_ami_usage_execution" {
  name_prefix = "lambda_policy"
  policy      = data.aws_iam_policy_document.monitor_ami_usage_execution.json
}

resource "aws_iam_role_policy_attachment" "monitor_ami_usage_execution" {
  role       = aws_iam_role.monitor_ami_usage_execution.name
  policy_arn = aws_iam_policy.monitor_ami_usage_execution.arn
}

data "archive_file" "monitor_ami_usage" {
  type        = "zip"
  source_file = "${path.module}/monitor_ami_usage.py"
  output_path = "${path.module}/monitor_ami_usage.zip"
}

#tfsec:ignore:avd-aws-0066
resource "aws_lambda_function" "monitor_ami_usage" {
  function_name    = "monitor_ami_usage_execution"
  handler          = "monitor_ami_usage.lambda_handler"
  role             = aws_iam_role.monitor_ami_usage_execution.arn
  runtime          = "python3.9"
  filename         = data.archive_file.monitor_ami_usage.output_path
  source_code_hash = data.archive_file.monitor_ami_usage.output_base64sha256
  tags             = local.tags
  timeout          = 60

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.account_alerts.arn
    }
  }
}

#tfsec:ignore:avd-aws-0017
resource "aws_cloudwatch_log_group" "monitor_ami_usage" {
  name              = "/aws/lambda/${aws_lambda_function.monitor_ami_usage.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_event_rule" "monitor_ami_usage" {
  name                = "monitor-ami-usage-trigger"
  description         = "Triggers Lambda at noon ET every day"
  schedule_expression = "cron(0 17 * * ? *)"
}

resource "aws_lambda_permission" "monitor_ami_usage" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monitor_ami_usage.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monitor_ami_usage.arn
}

resource "aws_cloudwatch_event_target" "monitor_ami_usage" {
  rule      = aws_cloudwatch_event_rule.monitor_ami_usage.name
  target_id = "invokeLambdaFunction"
  arn       = aws_lambda_function.monitor_ami_usage.arn
}
