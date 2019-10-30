#Manages s3 bucket
resource "aws_s3_bucket" "ops-vw-interns-climate-perception-tweets" {
  bucket = "ops-vw-interns-climate-perception-tweets"
  acl    = "private"
  cors_rule {
    allowed_headers = ["Authorization"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}
