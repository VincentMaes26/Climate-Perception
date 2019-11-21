# Notebook instance
resource "aws_sagemaker_notebook_instance" "Twitter-sentiment-analysis" {
  instance_type         = "ml.t2.large"
  lifecycle_config_name = "sm-notebook-conf"
  name                  = "Twitter-sentiment-analysis"
  role_arn              = "arn:aws:iam::916245739953:role/service-role/AmazonSageMaker-ExecutionRole-20191022T143324"
  tags                  = {}
}

# Lifecycle
resource "aws_sagemaker_notebook_instance_lifecycle_configuration" "sm-notebook-conf" {
  name = "sm-notebook-conf"
  #on_start = "IyEvYmluL2Jhc2gKc2V0IC1lCnN1ZG8gLXUgZWMyLXVzZXIgLWkgPDwnRU9GJwpFTlZJUk9OTUVOVD1weXRob24zCnNvdXJjZSAvaG9tZS9lYzItdXNlci9hbmFjb25kYTMvYmluL2FjdGl2YXRlICIkRU5WSVJPTk1FTlQiCnBpcCBpbnN0YWxsIC0tdXBncmFkZSBjdWZmbGlua3MgeWVsbG93YnJpY2sgd29yZGNsb3VkIGpvYmxpYgpzb3VyY2UgL2hvbWUvZWMyLXVzZXIvYW5hY29uZGEzL2Jpbi9kZWFjdGl2YXRlCkVPRg=="
  on_start = "${filebase64sha256("../notebook-lifecycle/script/sm-lifecycle-conf.zip")}"
}
