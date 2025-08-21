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
  type = list(object({
    accounts      = optional(list(string))
    finding_type  = string
    is_partial    = bool
    resources     = optional(list(string))
    resource_type = optional(string)
  }))
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

variable "service_quota_threshold" {
  default     = 80
  description = "The threshold percentage for service quota alerts"
  type        = number
}

variable "service_quota_region_list" {
  description = "List of regions to monitor for service quotas. Note that you cannot monitor across partitions (e.g. us-east-1 and us-gov-east-1)"
  type        = list(string)
  default     = ["us-east-1"]
}

variable "tags" {
  default     = {}
  description = "User-Defined tags"
  type        = map(string)
}

variable "sns_subscription_endpoint" {
  description = "HTTPS endpoint for SNS subscription. If not specified, defaults to Datadog webhook"
  type        = string
  default     = null
}
