#Manages s3 bucket
resource "aws_s3_bucket" "ops-vw-interns-climate-perception-tweets" {
  bucket        = "ops-vw-interns-climate-perception-tweets"
  request_payer = "BucketOwner"
  tags          = {}

  versioning {
    enabled    = false
    mfa_delete = false
  }
}
