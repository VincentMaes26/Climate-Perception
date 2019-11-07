# Notebook instance
resource "aws_sagemaker_notebook_instance" "Twitter-sentiment-analysis" {
  instance_type         = "ml.t2.medium"
  lifecycle_config_name = "sm-notebook-conf"
  name                  = "Twitter-sentiment-analysis"
  role_arn              = "arn:aws:iam::916245739953:role/service-role/AmazonSageMaker-ExecutionRole-20191022T143324"
  tags                  = {}
}

# Lifecycle
resource "aws_sagemaker_notebook_instance_lifecycle_configuration" "sm-notebook-conf" {
  name      = "sm-notebook-conf"
  on_create = "IyEvYmluL2Jhc2gKCnNldCAtZQo="
  on_start  = "IyEvYmluL2Jhc2gKCnN1ZG8gLXUgZWMyLXVzZXIgLWkgPDwnRU9GJwoKc291cmNlIGFjdGl2YXRlIHB5dGhvbjMKCnBpcCBpbnN0YWxsIHllbGxvd2JyaWNrIGN1ZmZsaW5rcwoKCnNvdXJjZSBkZWFjdGl2YXRlCgpFT0Y="
}
