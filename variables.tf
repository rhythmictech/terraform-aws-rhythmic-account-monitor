variable "tags" {
  default     = {}
  description = "User-Defined tags"
  type        = map(string)
}

variable "datadog_api_key_secret_arn" {
  description = "ARN of the AWS Secret containing the Datadog API key"
  type        = string
}

variable "enable_iam_access_analyzer" {
  default     = false
  description = "A boolean flag to enable/disable IAM Access Analyzer"
  type        = bool
}

variable "iam_analyzer_unused_access_age" {
  default     = 90
  description = "The age in days after which IAM access is considered unused."
  type        = number
}
