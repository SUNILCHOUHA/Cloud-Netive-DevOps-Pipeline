resource "aws_s3_bucket" "state_bucket" {
  bucket = "backend-state-eks"
  
  tags = {
    Name = "Backend"
  }
}