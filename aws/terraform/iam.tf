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

#resource "aws_iam_role_policy_attachment" "lambda-s3-full-access" {
#
#}
#
#resource "aws_iam_policy" "lambda-sagemaker-full-access" {
#
#}


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


#resource "aws_iam_role_policy_attachment" "lambda-s3-full-access-attach" {
#
#}
#
#resource "aws_iam_policy" "lambda-s3-full-access" {
#
#}



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
  path                  = "/service-role/"
  tags                  = {}
}

#resource "aws_iam_role_policy_attachment" "sagemaker-full-access-attach" {
#}
#
#resource "aws_iam_policy" "sagemaker-full-access" {
#
#}
