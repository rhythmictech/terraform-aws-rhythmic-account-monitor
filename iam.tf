resource "aws_accessanalyzer_analyzer" "analyzer" {
  count = var.enable_iam_access_analyzer ? 1 : 0

  analyzer_name = "${var.name_prefix}-unused-access-analyzer"
  type          = "ORGANIZATION_UNUSED_ACCESS"
  tags          = local.tags

  configuration {
    unused_access {
      unused_access_age = var.iam_analyzer_unused_access_age
    }
  }
}

resource "aws_accessanalyzer_archive_rule" "archive_rules" {
  count = var.enable_iam_access_analyzer ? length(var.iam_access_analyzer_archive_rules) : 0

  analyzer_name = aws_accessanalyzer_analyzer.analyzer[0].analyzer_name
  rule_name     = "archive-rule-${count.index}"

  filter {
    criteria = "resourceType"
    eq       = [var.iam_access_analyzer_archive_rules[count.index].resource_type]
  }

  filter {
    criteria = "resource"
    contains = var.iam_access_analyzer_archive_rules[count.index].is_partial ? [var.iam_access_analyzer_archive_rules[count.index].resource] : null
    eq       = !var.iam_access_analyzer_archive_rules[count.index].is_partial ? [var.iam_access_analyzer_archive_rules[count.index].resource] : null
  }

  filter {
    criteria = "findingType"
    eq       = [var.iam_access_analyzer_archive_rules[count.index].finding_type]
  }
}
