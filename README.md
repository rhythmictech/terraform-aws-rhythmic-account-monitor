# terraform-aws-rhythmic-account-monitor
Configures AWS health and account related notifications

This module is used to monitor AWS accounts and send notifications for various events including:
- AWS Backup and Vault Lock lifecycle changes
- AWS Organizations account lifecycle changes
- AWS PHD events
- IAM access analyzer unused permissions/resources findings
- Resources using missing AMIs
- Service Quota limits

[![tflint](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/tflint.yaml/badge.svg)](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/tflint.yaml)
[![trivy](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/trivy.yaml/badge.svg)](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/trivy.yaml)
[![yamllint](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/yamllint.yaml/badge.svg)](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/yamllint.yaml)
[![misspell](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/tflint.yaml/badge.svg)](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/tflint.yaml)
[![pre-commit-check](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/rhythmictech/terraform-aws-rhythmic-account-monitor/actions/workflows/pre-commit.yaml)
<a href="https://twitter.com/intent/follow?screen_name=RhythmicTech"><img src="https://img.shields.io/twitter/follow/RhythmicTech?style=social&logo=twitter" alt="follow on Twitter"></a>

## Example
Here's what using the module will look like
```hcl
module "example" {
  source = "rhythmictech/rhythmic-account-monitor/aws"
  datadog_api_key_secret_arn = ""
}
```

## About
Rhythmic is an AWS Managed Services Provider. We rely heavily on automation to deliver our services, ingesting configuration, event and state information from AWS via listeners (e.g., EventBridge and SNS), services (e.g., Anomaly Detection), and APIs via custom scripts (e.g., Trusted Advisor).

We open source the vast majority of the resources we use to deliver our managed services because transparency is one of our principles.

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5 |
| <a name="requirement_archive"></a> [archive](#requirement\_archive) | >= 2.5.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.40 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.7.1 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.8.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_tags"></a> [tags](#module\_tags) | rhythmictech/tags/terraform | ~> 1.1.1 |

## Resources

| Name | Type |
|------|------|
| [aws_accessanalyzer_analyzer.unused_access_analyzer](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/accessanalyzer_analyzer) | resource |
| [aws_accessanalyzer_archive_rule.archive_rules](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/accessanalyzer_archive_rule) | resource |
| [aws_cloudwatch_event_rule.backup](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.backup_event](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.backup_vaultlock](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.control_tower](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.glacier_vaultlock](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.health](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.monitor_ami_usage](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.monitor_service_quotas](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_rule.organizations](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.backup](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.backup_event](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.backup_vaultlock](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.control_tower](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.glacier_vaultlock](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.health](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.monitor_ami_usage](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.monitor_service_quotas](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.organizations](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.monitor_ami_usage](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_group.monitor_service_quotas](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_iam_policy.monitor_ami_usage_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_policy.monitor_service_quotas_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.monitor_ami_usage_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role.monitor_service_quotas_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.monitor_ami_usage_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.monitor_service_quotas_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.monitor_service_quotas_security_analyst](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.monitor_ami_usage](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.monitor_service_quotas](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.monitor_ami_usage](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_lambda_permission.monitor_service_quotas](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [aws_sns_topic.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) | resource |
| [aws_sns_topic_policy.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_policy) | resource |
| [aws_sns_topic_subscription.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription) | resource |
| [archive_file.monitor_ami_usage](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [archive_file.monitor_service_quotas](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambda_assume](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.monitor_ami_usage_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.monitor_service_quotas_execution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_kms_alias.notifications](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/kms_alias) | data source |
| [aws_partition.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/partition) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |
| [aws_secretsmanager_secret.datadog_api_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret) | data source |
| [aws_secretsmanager_secret_version.datadog_api_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret_version) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_datadog_api_key_secret_arn"></a> [datadog\_api\_key\_secret\_arn](#input\_datadog\_api\_key\_secret\_arn) | ARN of the AWS Secret containing the Datadog API key | `string` | n/a | yes |
| <a name="input_enable_iam_access_analyzer"></a> [enable\_iam\_access\_analyzer](#input\_enable\_iam\_access\_analyzer) | A boolean flag to enable/disable IAM Access Analyzer | `bool` | `false` | no |
| <a name="input_enable_iam_access_analyzer_organization"></a> [enable\_iam\_access\_analyzer\_organization](#input\_enable\_iam\_access\_analyzer\_organization) | A boolean flag to enable/disable IAM Access Analyzer at the organization level (requires enable\_iam\_access\_analyzer to be true and IAM Access Analyzer to be enabled at the organization level) | `bool` | `false` | no |
| <a name="input_iam_access_analyzer_unused_archive_rules"></a> [iam\_access\_analyzer\_unused\_archive\_rules](#input\_iam\_access\_analyzer\_unused\_archive\_rules) | List of IAM resources to auto-archive unused access findings for | <pre>list(object({<br/>    accounts      = optional(list(string))<br/>    finding_type  = string<br/>    is_partial    = bool<br/>    resources     = optional(list(string))<br/>    resource_type = optional(string)<br/>  }))</pre> | `[]` | no |
| <a name="input_iam_analyzer_unused_access_age"></a> [iam\_analyzer\_unused\_access\_age](#input\_iam\_analyzer\_unused\_access\_age) | The age in days after which IAM access is considered unused. | `number` | `90` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | Prefix for all resource names | `string` | `"rhythmic-"` | no |
| <a name="input_notify_ec2_missing_ami"></a> [notify\_ec2\_missing\_ami](#input\_notify\_ec2\_missing\_ami) | Whether to notify when EC2 instances are using missing AMIs | `bool` | `false` | no |
| <a name="input_notify_ec2_missing_ami_if_snapshot_exists"></a> [notify\_ec2\_missing\_ami\_if\_snapshot\_exists](#input\_notify\_ec2\_missing\_ami\_if\_snapshot\_exists) | Whether to notify when EC2 instances are using missing AMIs but snapshots exist | `bool` | `true` | no |
| <a name="input_service_quota_region_list"></a> [service\_quota\_region\_list](#input\_service\_quota\_region\_list) | List of regions to monitor for service quotas. Note that you cannot monitor across partitions (e.g. us-east-1 and us-gov-east-1) | `list(string)` | <pre>[<br/>  "us-east-1"<br/>]</pre> | no |
| <a name="input_service_quota_threshold"></a> [service\_quota\_threshold](#input\_service\_quota\_threshold) | The threshold percentage for service quota alerts | `number` | `80` | no |
| <a name="input_sns_subscription_endpoint"></a> [sns\_subscription\_endpoint](#input\_sns\_subscription\_endpoint) | HTTPS endpoint for SNS subscription. If not specified, defaults to Datadog webhook | `string` | `null` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | User-Defined tags | `map(string)` | `{}` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->

## Getting Started
This workflow has a few prerequisites which are installed through the `./bin/install-x.sh` scripts and are linked below. The install script will also work on your local machine.

- [pre-commit](https://pre-commit.com)
- [terraform](https://terraform.io)
- [tfenv](https://github.com/tfutils/tfenv)
- [terraform-docs](https://github.com/segmentio/terraform-docs)
- [tfsec](https://github.com/tfsec/tfsec)
- [tflint](https://github.com/terraform-linters/tflint)

We use `tfenv` to manage `terraform` versions, so the version is defined in the `versions.tf` and `tfenv` installs the latest compliant version.
`pre-commit` is like a package manager for scripts that integrate with git hooks. We use them to run the rest of the tools before apply.
`terraform-docs` creates the beautiful docs (above),  `tfsec` scans for security no-nos, `tflint` scans for best practices.
