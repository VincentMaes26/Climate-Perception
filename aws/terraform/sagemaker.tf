# Notebook instance
resource "aws_sagemaker_notebook_instance" "Twitter-sentiment-analysis" {
  instance_type         = "ml.t2.medium"
  lifecycle_config_name = "sm-notebook-conf"
  name                  = "Twitter-sentiment-analysis"
  role_arn              = "arn:aws:iam::916245739953:role/service-role/AmazonSageMaker-ExecutionRole-20191022T143324"
  tags                  = {}
}

# Lifecycle
#resource "aws_sagemaker_notebook_instance_lifecycle_configuration" "sm-notebook-conf" {
#
#}
#
#data "template_file" "instance-init" {
#
#}
