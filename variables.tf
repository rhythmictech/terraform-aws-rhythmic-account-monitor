variable "tags" {
  default     = {}
  description = "User-Defined tags"
  type        = map(string)
}

variable "datadog_api_key_secret_arn" {
  description = "ARN of the AWS Secret containing the Datadog API key"
  type        = string
}

########################################
# Anomaly Detection Vars
########################################
variable "anomaly_total_impact_absolute_threshold" {
  description = "Minimum dollar threshold"
  type        = number
  default     = 100
}

variable "anomaly_total_impact_percentage_threshold" {
  description = "Percentage threshold"
  type        = number
  default     = 10
}

########################################
# Budget Vars
########################################
variable "monitor_ri_utilization" {
  description = "Enable monitoring of Reserverd Instances Utilization"
  type        = bool
  default     = false
}

variable "monitor_sp_utilization" {
  description = "Enable monitoring of Savings Plan Utilization"
  type        = bool
  default     = false
}

variable "ri_utilization_services" {
  default     = ["ec2", "elasticache", "es", "opensearch", "rds", "redshift"]
  description = "List of services for Reserved Instance utilization monitoring"
  type        = list(string)
}

variable "service_budgets" {
  default = {
    "ec2" = {
      time_unit         = "MONTHLY"
      limit_amount      = "5" # Adjust this value based on your budget
      limit_unit        = "USD"
      threshold         = 90 # Notify when spending exceeds 90% of the budget
      threshold_type    = "PERCENTAGE"
      notification_type = "ACTUAL"
    }
  }
  description = "Map of service budgets"
  type = map(object({
    time_unit : string
    limit_amount : string
    limit_unit : string
    threshold : number
    threshold_type : string
    notification_type : string
  }))

}

variable "aws_service_shorthand_map" {
  description = "Map of shorthand notation for AWS services to their long form AWS services in cost and usage reporting, sorted alphabetically with lowercase keys"
  type        = map(string)
  default = {
    "apiGateway"          = "Amazon API Gateway",
    "appFlow"             = "Amazon AppFlow",
    "appRunner"           = "AWS App Runner",
    "appSync"             = "AWS AppSync",
    "athena"              = "Amazon Athena",
    "backup"              = "AWS Backup",
    "braket"              = "Amazon Braket",
    "chime"               = "Amazon Chime",
    "cloudFront"          = "Amazon CloudFront",
    "cloudWatch"          = "Amazon CloudWatch",
    "codeArtifact"        = "AWS CodeArtifact",
    "codeBuild"           = "AWS CodeBuild",
    "codeCommit"          = "AWS CodeCommit",
    "codeDeploy"          = "AWS CodeDeploy",
    "codePipeline"        = "AWS CodePipeline",
    "codeStar"            = "AWS CodeStar",
    "comprehend"          = "Amazon Comprehend",
    "connect"             = "Amazon Connect",
    "dataPipeline"        = "AWS Data Pipeline",
    "datadog"             = "Datadog",
    "deepComposer"        = "AWS DeepComposer",
    "deepLens"            = "AWS DeepLens",
    "deepRacer"           = "AWS DeepRacer",
    "detective"           = "Amazon Detective",
    "directConnect"       = "AWS Direct Connect",
    "documentDB"          = "Amazon DocumentDB",
    "dms"                 = "AWS Database Migration Service",
    "dynamodb"            = "Amazon DynamoDB",
    "ec2"                 = "Amazon Elastic Compute Cloud - Compute",
    "ecs"                 = "Amazon Elastic Container Service",
    "efs"                 = "Amazon Elastic File System",
    "eks"                 = "Amazon Elastic Kubernetes Service",
    "elasticache"         = "Amazon ElastiCache",
    "emr"                 = "Amazon Elastic MapReduce",
    "es"                  = "Amazon Elasticsearch Service",
    "fargate"             = "AWS Fargate",
    "forecast"            = "Amazon Forecast",
    "fsx"                 = "Amazon FSx",
    "gameLift"            = "Amazon GameLift",
    "glue"                = "AWS Glue",
    "greengrass"          = "AWS Greengrass",
    "guardDuty"           = "Amazon GuardDuty",
    "healthLake"          = "Amazon HealthLake",
    "honeycode"           = "Amazon Honeycode",
    "iam"                 = "AWS Identity and Access Management",
    "inspector"           = "Amazon Inspector",
    "iot1Click"           = "AWS IoT 1-Click",
    "iotAnalytics"        = "AWS IoT Analytics",
    "iotButton"           = "AWS IoT Button",
    "iotCore"             = "AWS IoT Core",
    "iotDeviceManagement" = "AWS IoT Device Management",
    "iotEvents"           = "AWS IoT Events",
    "iotSiteWise"         = "AWS IoT SiteWise",
    "iotThingsGraph"      = "AWS IoT Things Graph",
    "ivs"                 = "Amazon Interactive Video Service",
    "kendra"              = "Amazon Kendra",
    "kinesis"             = "Amazon Kinesis",
    "kms"                 = "AWS Key Management Service",
    "lambda"              = "AWS Lambda",
    "lex"                 = "Amazon Lex",
    "lightsail"           = "Amazon Lightsail",
    "lookoutForVision"    = "Amazon Lookout for Vision",
    "lumberyard"          = "Amazon Lumberyard",
    "macie"               = "Amazon Macie",
    "managedBlockchain"   = "Amazon Managed Blockchain",
    "mq"                  = "Amazon MQ",
    "msk"                 = "Amazon Managed Streaming for Apache Kafka",
    "neptune"             = "Amazon Neptune",
    "opensearch"          = "Amazon OpenSearch Service",
    "outposts"            = "AWS Outposts",
    "pinpoint"            = "Amazon Pinpoint",
    "polly"               = "Amazon Polly",
    "qldb"                = "Amazon Quantum Ledger Database",
    "qls"                 = "AWS Quantum Ledger Service",
    "quicksight"          = "Amazon QuickSight",
    "rds"                 = "Amazon Relational Database Service",
    "redshift"            = "Amazon Redshift",
    "rekognition"         = "Amazon Rekognition",
    "robomaker"           = "AWS RoboMaker",
    "route53"             = "Amazon Route 53",
    "s3"                  = "Amazon Simple Storage Service",
    "s3Outposts"          = "Amazon S3 on Outposts",
    "sagemaker"           = "Amazon SageMaker",
    "ses"                 = "Amazon Simple Email Service",
    "sesv2"               = "Amazon Simple Email Service v2",
    "shield"              = "AWS Shield",
    "sns"                 = "Amazon Simple Notification Service",
    "snowball"            = "AWS Snowball",
    "sqs"                 = "Amazon Simple Queue Service",
    "stepFunctions"       = "AWS Step Functions",
    "storageGateway"      = "AWS Storage Gateway",
    "sumerian"            = "Amazon Sumerian",
    "swf"                 = "Amazon Simple Workflow Service",
    "textract"            = "Amazon Textract",
    "timestream"          = "Amazon Timestream",
    "transcribe"          = "Amazon Transcribe",
    "transcribeMedical"   = "Amazon Transcribe Medical",
    "translate"           = "Amazon Translate",
    "transfer"            = "AWS Transfer for SFTP",
    "vpn"                 = "AWS VPN",
    "waf"                 = "AWS WAF",
    "wellArchitectedTool" = "AWS Well-Architected Tool",
    "workDocs"            = "Amazon WorkDocs",
    "workLink"            = "Amazon WorkLink",
    "workMail"            = "Amazon WorkMail",
    "workSpaces"          = "Amazon WorkSpaces",
    "xRay"                = "AWS X-Ray",
    "zocalo"              = "Amazon Zocalo"
  }
}

# Cost and Usage aggregation vars
variable "enable_cur_forwarding" {
  description = "Enable Cost and Usage Report forwarding. Do not enable unless `enable_cur_collection` is also enabled."
  type        = bool
  default     = false
}

variable "enable_cur_collection" {
  description = "Enable Cost and Usage Report collection. Be mindful of existing CUR collection processes before enabling."
  type        = bool
  default     = false
}

variable "enable_datadog_cost_management" {
  default     = false
  description = "Enable Datadog cost management"
  type        = bool
}

variable "cur_forwarding_bucket_arn" {
  default     = null
  description = "S3 bucket ARN where CUR data will be forwarded"
  type        = string
}
