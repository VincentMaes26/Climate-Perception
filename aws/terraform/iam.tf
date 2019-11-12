# Notebook activity monitor lambda
resource "aws_iam_role" "notebook-activity-monitor-role" {
  assume_role_policy    = jsonencode(
      {
          Statement = [
              {
                  Action    = "sts:AssumeRole"
                  Effect    = "Allow"
                  Principal = {
                      Service = "lambda.amazonaws.com"
                  }
              },
          ]
          Version   = "2012-10-17"
      }
  )
  force_detach_policies = false
  max_session_duration  = 3600
  path                  = "/service-role/"
  tags                  = {}
}

resource "aws_iam_role_policy_attachment" "lambda-sagemaker-full-access-attachment" {
  role       = "${aws_iam_role.notebook-activity-monitor-role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}


# Tweet collector lambda
resource "aws_iam_role" "tweet-collector-role" {
  assume_role_policy    = jsonencode(
      {
          Statement = [
              {
                  Action    = "sts:AssumeRole"
                  Effect    = "Allow"
                  Principal = {
                      Service = "lambda.amazonaws.com"
                  }
              },
          ]
          Version   = "2012-10-17"
      }
  )
  force_detach_policies = false
  max_session_duration  = 3600
  path                  = "/service-role/"
  tags                  = {}
}

resource "aws_iam_role_policy_attachment" "lambda-s3-full-access-attach" {
  role = "${aws_iam_role.tweet-collector-role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda-secretmanager-read-write-attach" {
    role = "${aws_iam_role.tweet-collector-role.name}"
    policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}


# sagemaker notebook
resource "aws_iam_role" "sagemaker-role" {
  assume_role_policy    = jsonencode(
      {
          Statement = [
              {
                  Action    = "sts:AssumeRole"
                  Effect    = "Allow"
                  Principal = {
                      Service = "sagemaker.amazonaws.com"
                  }
              },
          ]
          Version   = "2012-10-17"
      }
  )
  force_detach_policies = false
  max_session_duration  = 3600
  name                  = "AmazonSageMaker-ExecutionRole-20191022T143324"
  description           = "SageMaker execution role created from the SageMaker AWS Management Console."
  path                  = "/service-role/"
  tags                  = {}
}

resource "aws_iam_role_policy_attachment" "sagemaker-full-access-attach" {
  role       = "${aws_iam_role.sagemaker-role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
