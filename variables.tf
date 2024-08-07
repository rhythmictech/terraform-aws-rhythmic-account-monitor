variable "datadog_api_key_secret_arn" {
  description = "ARN of the AWS Secret containing the Datadog API key"
  type        = string
}

variable "enable_iam_access_analyzer" {
  default     = false
  description = "A boolean flag to enable/disable IAM Access Analyzer"
  type        = bool
}

variable "enable_iam_access_analyzer_organization" {
  default     = false
  description = "A boolean flag to enable/disable IAM Access Analyzer at the organization level (requires enable_iam_access_analyzer to be true and IAM Access Analyzer to be enabled at the organization level)"
  type        = bool
}

variable "iam_access_analyzer_unused_archive_rules" {
  default     = []
  description = "List of IAM resources to auto-archive unused access findings for"
  type        = list(any)
}

variable "iam_analyzer_unused_access_age" {
  default     = 90
  description = "The age in days after which IAM access is considered unused."
  type        = number
}


variable "name_prefix" {
  default     = "rhythmic-"
  description = "Prefix for all resource names"
  type        = string
}

variable "notify_ec2_missing_ami" {
  description = "Whether to notify when EC2 instances are using missing AMIs"
  type        = bool
  default     = false
}

variable "notify_ec2_missing_ami_if_snapshot_exists" {
  description = "Whether to notify when EC2 instances are using missing AMIs but snapshots exist"
  type        = bool
  default     = true
}

variable "tags" {
  default     = {}
  description = "User-Defined tags"
  type        = map(string)
}
