# Notebook instance
resource "aws_sagemaker_notebook_instance" "Twitter-sentiment-analysis" {
  instance_type         = "ml.t2.2xlarge"
  lifecycle_config_name = "sm-notebook-conf"
  name                  = "Twitter-sentiment-analysis"
  role_arn              = "arn:aws:iam::916245739953:role/service-role/AmazonSageMaker-ExecutionRole-20191022T143324"
  tags                  = {}
}

# Lifecycle
resource "aws_sagemaker_notebook_instance_lifecycle_configuration" "sm-notebook-conf" {
  name = "sm-notebook-conf"
  on_start = "IyEvYmluL2Jhc2gKCnN1ZG8gLXUgZWMyLXVzZXIgLWkgPDwnRU9GJwpzb3VyY2UgYWN0aXZhdGUgcHl0aG9uMwpwaXAgaW5zdGFsbCAtLXVwZ3JhZGUgY3VmZmxpbmtzIHllbGxvd2JyaWNrIHdvcmRjbG91ZCBqb2JsaWIgeGdib29zdApzb3VyY2UgZGVhY3RpdmF0ZQoKRU9G"
}
