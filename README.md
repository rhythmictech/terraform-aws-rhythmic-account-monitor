# terraform-aws-rhythmic-account-monitor
Configures AWS health and account related notifications

[![tflint](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/workflows/tflint/badge.svg?branch=master&event=push)](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/actions?query=workflow%3Atflint+event%3Apush+branch%3Amaster)
[![tfsec](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/workflows/tfsec/badge.svg?branch=master&event=push)](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/actions?query=workflow%3Atfsec+event%3Apush+branch%3Amaster)
[![yamllint](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/workflows/yamllint/badge.svg?branch=master&event=push)](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/actions?query=workflow%3Ayamllint+event%3Apush+branch%3Amaster)
[![misspell](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/workflows/misspell/badge.svg?branch=master&event=push)](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/actions?query=workflow%3Amisspell+event%3Apush+branch%3Amaster)
[![pre-commit-check](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/workflows/pre-commit-check/badge.svg?branch=master&event=push)](https://github.com/rhythmictech/terraform-aws-rhythmic-cost-monitor/actions?query=workflow%3Apre-commit-check+event%3Apush+branch%3Amaster)
<a href="https://twitter.com/intent/follow?screen_name=RhythmicTech"><img src="https://img.shields.io/twitter/follow/RhythmicTech?style=social&logo=twitter" alt="follow on Twitter"></a>

## Example
Here's what using the module will look like
```hcl
module "example" {
  source = "rhythmictech/terraform-aws-rhythmic-cost-monitor
  datadog_api_key_secret_arn = ""
}
```

## About
A bit about this module

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.62 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.36.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_tags"></a> [tags](#module\_tags) | rhythmictech/tags/terraform | ~> 1.1.1 |

## Resources

| Name | Type |
|------|------|
| [aws_sns_topic.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic) | resource |
| [aws_sns_topic_policy.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_policy) | resource |
| [aws_sns_topic_subscription.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.account_alerts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |
| [aws_secretsmanager_secret.datadog_api_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret) | data source |
| [aws_secretsmanager_secret_version.datadog_api_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/secretsmanager_secret_version) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_anomaly_total_impact_absolute_threshold"></a> [anomaly\_total\_impact\_absolute\_threshold](#input\_anomaly\_total\_impact\_absolute\_threshold) | Minimum dollar threshold | `number` | `100` | no |
| <a name="input_anomaly_total_impact_percentage_threshold"></a> [anomaly\_total\_impact\_percentage\_threshold](#input\_anomaly\_total\_impact\_percentage\_threshold) | Percentage threshold | `number` | `10` | no |
| <a name="input_aws_service_shorthand_map"></a> [aws\_service\_shorthand\_map](#input\_aws\_service\_shorthand\_map) | Map of shorthand notation for AWS services to their long form AWS services in cost and usage reporting, sorted alphabetically with lowercase keys | `map(string)` | <pre>{<br>  "apiGateway": "Amazon API Gateway",<br>  "appFlow": "Amazon AppFlow",<br>  "appRunner": "AWS App Runner",<br>  "appSync": "AWS AppSync",<br>  "athena": "Amazon Athena",<br>  "backup": "AWS Backup",<br>  "braket": "Amazon Braket",<br>  "chime": "Amazon Chime",<br>  "cloudFront": "Amazon CloudFront",<br>  "cloudWatch": "Amazon CloudWatch",<br>  "codeArtifact": "AWS CodeArtifact",<br>  "codeBuild": "AWS CodeBuild",<br>  "codeCommit": "AWS CodeCommit",<br>  "codeDeploy": "AWS CodeDeploy",<br>  "codePipeline": "AWS CodePipeline",<br>  "codeStar": "AWS CodeStar",<br>  "comprehend": "Amazon Comprehend",<br>  "connect": "Amazon Connect",<br>  "dataPipeline": "AWS Data Pipeline",<br>  "datadog": "Datadog",<br>  "deepComposer": "AWS DeepComposer",<br>  "deepLens": "AWS DeepLens",<br>  "deepRacer": "AWS DeepRacer",<br>  "detective": "Amazon Detective",<br>  "directConnect": "AWS Direct Connect",<br>  "dms": "AWS Database Migration Service",<br>  "documentDB": "Amazon DocumentDB",<br>  "dynamodb": "Amazon DynamoDB",<br>  "ec2": "Amazon Elastic Compute Cloud - Compute",<br>  "ecs": "Amazon Elastic Container Service",<br>  "efs": "Amazon Elastic File System",<br>  "eks": "Amazon Elastic Kubernetes Service",<br>  "elasticache": "Amazon ElastiCache",<br>  "emr": "Amazon Elastic MapReduce",<br>  "es": "Amazon Elasticsearch Service",<br>  "fargate": "AWS Fargate",<br>  "forecast": "Amazon Forecast",<br>  "fsx": "Amazon FSx",<br>  "gameLift": "Amazon GameLift",<br>  "glue": "AWS Glue",<br>  "greengrass": "AWS Greengrass",<br>  "guardDuty": "Amazon GuardDuty",<br>  "healthLake": "Amazon HealthLake",<br>  "honeycode": "Amazon Honeycode",<br>  "iam": "AWS Identity and Access Management",<br>  "inspector": "Amazon Inspector",<br>  "iot1Click": "AWS IoT 1-Click",<br>  "iotAnalytics": "AWS IoT Analytics",<br>  "iotButton": "AWS IoT Button",<br>  "iotCore": "AWS IoT Core",<br>  "iotDeviceManagement": "AWS IoT Device Management",<br>  "iotEvents": "AWS IoT Events",<br>  "iotSiteWise": "AWS IoT SiteWise",<br>  "iotThingsGraph": "AWS IoT Things Graph",<br>  "ivs": "Amazon Interactive Video Service",<br>  "kendra": "Amazon Kendra",<br>  "kinesis": "Amazon Kinesis",<br>  "kms": "AWS Key Management Service",<br>  "lambda": "AWS Lambda",<br>  "lex": "Amazon Lex",<br>  "lightsail": "Amazon Lightsail",<br>  "lookoutForVision": "Amazon Lookout for Vision",<br>  "lumberyard": "Amazon Lumberyard",<br>  "macie": "Amazon Macie",<br>  "managedBlockchain": "Amazon Managed Blockchain",<br>  "mq": "Amazon MQ",<br>  "msk": "Amazon Managed Streaming for Apache Kafka",<br>  "neptune": "Amazon Neptune",<br>  "opensearch": "Amazon OpenSearch Service",<br>  "outposts": "AWS Outposts",<br>  "pinpoint": "Amazon Pinpoint",<br>  "polly": "Amazon Polly",<br>  "qldb": "Amazon Quantum Ledger Database",<br>  "qls": "AWS Quantum Ledger Service",<br>  "quicksight": "Amazon QuickSight",<br>  "rds": "Amazon Relational Database Service",<br>  "redshift": "Amazon Redshift",<br>  "rekognition": "Amazon Rekognition",<br>  "robomaker": "AWS RoboMaker",<br>  "route53": "Amazon Route 53",<br>  "s3": "Amazon Simple Storage Service",<br>  "s3Outposts": "Amazon S3 on Outposts",<br>  "sagemaker": "Amazon SageMaker",<br>  "ses": "Amazon Simple Email Service",<br>  "sesv2": "Amazon Simple Email Service v2",<br>  "shield": "AWS Shield",<br>  "snowball": "AWS Snowball",<br>  "sns": "Amazon Simple Notification Service",<br>  "sqs": "Amazon Simple Queue Service",<br>  "stepFunctions": "AWS Step Functions",<br>  "storageGateway": "AWS Storage Gateway",<br>  "sumerian": "Amazon Sumerian",<br>  "swf": "Amazon Simple Workflow Service",<br>  "textract": "Amazon Textract",<br>  "timestream": "Amazon Timestream",<br>  "transcribe": "Amazon Transcribe",<br>  "transcribeMedical": "Amazon Transcribe Medical",<br>  "transfer": "AWS Transfer for SFTP",<br>  "translate": "Amazon Translate",<br>  "vpn": "AWS VPN",<br>  "waf": "AWS WAF",<br>  "wellArchitectedTool": "AWS Well-Architected Tool",<br>  "workDocs": "Amazon WorkDocs",<br>  "workLink": "Amazon WorkLink",<br>  "workMail": "Amazon WorkMail",<br>  "workSpaces": "Amazon WorkSpaces",<br>  "xRay": "AWS X-Ray",<br>  "zocalo": "Amazon Zocalo"<br>}</pre> | no |
| <a name="input_cur_forwarding_bucket_arn"></a> [cur\_forwarding\_bucket\_arn](#input\_cur\_forwarding\_bucket\_arn) | S3 bucket ARN where CUR data will be forwarded | `string` | `null` | no |
| <a name="input_datadog_api_key_secret_arn"></a> [datadog\_api\_key\_secret\_arn](#input\_datadog\_api\_key\_secret\_arn) | ARN of the AWS Secret containing the Datadog API key | `string` | n/a | yes |
| <a name="input_enable_cur_collection"></a> [enable\_cur\_collection](#input\_enable\_cur\_collection) | Enable Cost and Usage Report collection. Be mindful of existing CUR collection processes before enabling. | `bool` | `false` | no |
| <a name="input_enable_cur_forwarding"></a> [enable\_cur\_forwarding](#input\_enable\_cur\_forwarding) | Enable Cost and Usage Report forwarding. Do not enable unless `enable_cur_collection` is also enabled. | `bool` | `false` | no |
| <a name="input_enable_datadog_cost_management"></a> [enable\_datadog\_cost\_management](#input\_enable\_datadog\_cost\_management) | Enable Datadog cost management | `bool` | `false` | no |
| <a name="input_monitor_ri_utilization"></a> [monitor\_ri\_utilization](#input\_monitor\_ri\_utilization) | Enable monitoring of Reserverd Instances Utilization | `bool` | `false` | no |
| <a name="input_monitor_sp_utilization"></a> [monitor\_sp\_utilization](#input\_monitor\_sp\_utilization) | Enable monitoring of Savings Plan Utilization | `bool` | `false` | no |
| <a name="input_ri_utilization_services"></a> [ri\_utilization\_services](#input\_ri\_utilization\_services) | List of services for Reserved Instance utilization monitoring | `list(string)` | <pre>[<br>  "ec2",<br>  "elasticache",<br>  "es",<br>  "opensearch",<br>  "rds",<br>  "redshift"<br>]</pre> | no |
| <a name="input_service_budgets"></a> [service\_budgets](#input\_service\_budgets) | Map of service budgets | <pre>map(object({<br>    time_unit       : string<br>    limit_amount    : string<br>    limit_unit      : string<br>    threshold       : number<br>    threshold_type  : string<br>    notification_type : string<br>  }))</pre> | <pre>{<br>  "ec2": {<br>    "limit_amount": "5",<br>    "limit_unit": "USD",<br>    "notification_type": "ACTUAL",<br>    "threshold": 90,<br>    "threshold_type": "PERCENTAGE",<br>    "time_unit": "MONTHLY"<br>  }<br>}</pre> | no |
| <a name="input_tags"></a> [tags](#input\_tags) | User-Defined tags | `map(string)` | `{}` | no |

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

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
