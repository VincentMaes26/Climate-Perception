# Notebook instance
resource "aws_sagemaker_notebook_instance" "Twitter-sentiment-analysis" {

}

# Lifecycle
resource "aws_sagemaker_notebook_instance_lifecycle_configuration" "sm-notebook-conf" {

}

data "template_file" "instance-init" {

}
