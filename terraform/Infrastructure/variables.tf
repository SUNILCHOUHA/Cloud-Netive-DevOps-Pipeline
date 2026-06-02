variable "aws_region" {
  default = "ap-south-1"
}

variable "db_username" {
  default = "postgres"
}

variable "db_password" {
  type = string
  sensitive = true
}
