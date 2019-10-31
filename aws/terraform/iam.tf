# Notebook activity monitor lambda
resource "aws_iam_role" "notebook-activity-monitor-role" {

}

resource "aws_iam_role_policy_attachment" "lambda-s3-full-access" {

}

resource "aws_iam_policy" "lambda-sagemaker-full-access" {

}


# Tweet collector lambda
resource "aws_iam_role" "tweet-collector-role" {

}


resource "aws_iam_role_policy_attachment" "lambda-s3-full-access-attach" {

}

resource "aws_iam_policy" "lambda-s3-full-access" {

}

resource "aws_iam_role" "sagemaker-role" {

}


# sagemaker notebook
resource "aws_iam_role_policy_attachment" "sagemaker-full-access-attach" {
}

resource "aws_iam_policy" "sagemaker-full-access" {

}
