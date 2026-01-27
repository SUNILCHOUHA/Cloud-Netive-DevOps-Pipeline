terraform {
  required_version = ">= 1.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  

  backend "s3" {
    bucket         = "backend-state-eks"
    key            = "terraform/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile = true
    # dynamodb_table = "State-lock"
    encrypt        = true
  }
}
