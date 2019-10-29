# Lambda function
resource "aws_lambda_function" "notebook-activity-monitor" {
  function_name = "notebook-activity-monitor"
  handler       = "lambda_function.lambda_handler"
  runtime       = "Python 3.7"
  role          = "${aws_iam_role.notebook-activity-monitor-role}"
}

# IAM
resource "aws_iam_role" "notebook-activity-monitor-role" {
  name = "notebook-activity-monitor-role-8v4m1pyc"

  assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:eu-west-1:916245739953:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:eu-west-1:916245739953:log-group:/aws/lambda/notebook-activity-monitor:*"
            ]
        }
    ]
  }
  EOF

}

resource "aws_iam_role_policy_attachment" "lambda-s3-full-access" {
  role       = "${aws_iam_role.notebook-activity-monitor-role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_policy" "lambda-sagemaker-full-access" {
  assume_role_policy = <<EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "sagemaker:*"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "application-autoscaling:DeleteScalingPolicy",
                  "application-autoscaling:DeleteScheduledAction",
                  "application-autoscaling:DeregisterScalableTarget",
                  "application-autoscaling:DescribeScalableTargets",
                  "application-autoscaling:DescribeScalingActivities",
                  "application-autoscaling:DescribeScalingPolicies",
                  "application-autoscaling:DescribeScheduledActions",
                  "application-autoscaling:PutScalingPolicy",
                  "application-autoscaling:PutScheduledAction",
                  "application-autoscaling:RegisterScalableTarget",
                  "aws-marketplace:ViewSubscriptions",
                  "cloudwatch:DeleteAlarms",
                  "cloudwatch:DescribeAlarms",
                  "cloudwatch:GetMetricData",
                  "cloudwatch:GetMetricStatistics",
                  "cloudwatch:ListMetrics",
                  "cloudwatch:PutMetricAlarm",
                  "cloudwatch:PutMetricData",
                  "codecommit:BatchGetRepositories",
                  "codecommit:CreateRepository",
                  "codecommit:GetRepository",
                  "codecommit:ListBranches",
                  "codecommit:ListRepositories",
                  "cognito-idp:AdminAddUserToGroup",
                  "cognito-idp:AdminCreateUser",
                  "cognito-idp:AdminDeleteUser",
                  "cognito-idp:AdminDisableUser",
                  "cognito-idp:AdminEnableUser",
                  "cognito-idp:AdminRemoveUserFromGroup",
                  "cognito-idp:CreateGroup",
                  "cognito-idp:CreateUserPool",
                  "cognito-idp:CreateUserPoolClient",
                  "cognito-idp:CreateUserPoolDomain",
                  "cognito-idp:DescribeUserPool",
                  "cognito-idp:DescribeUserPoolClient",
                  "cognito-idp:ListGroups",
                  "cognito-idp:ListIdentityProviders",
                  "cognito-idp:ListUserPoolClients",
                  "cognito-idp:ListUserPools",
                  "cognito-idp:ListUsers",
                  "cognito-idp:ListUsersInGroup",
                  "cognito-idp:UpdateUserPool",
                  "cognito-idp:UpdateUserPoolClient",
                  "ec2:CreateNetworkInterface",
                  "ec2:CreateNetworkInterfacePermission",
                  "ec2:CreateVpcEndpoint",
                  "ec2:DeleteNetworkInterface",
                  "ec2:DeleteNetworkInterfacePermission",
                  "ec2:DescribeDhcpOptions",
                  "ec2:DescribeNetworkInterfaces",
                  "ec2:DescribeRouteTables",
                  "ec2:DescribeSecurityGroups",
                  "ec2:DescribeSubnets",
                  "ec2:DescribeVpcEndpoints",
                  "ec2:DescribeVpcs",
                  "ecr:BatchCheckLayerAvailability",
                  "ecr:BatchGetImage",
                  "ecr:CreateRepository",
                  "ecr:Describe*",
                  "ecr:GetAuthorizationToken",
                  "ecr:GetDownloadUrlForLayer",
                  "elastic-inference:Connect",
                  "elasticfilesystem:DescribeFileSystems",
                  "elasticfilesystem:DescribeMountTargets",
                  "fsx:DescribeFileSystems",
                  "glue:CreateJob",
                  "glue:DeleteJob",
                  "glue:GetJob",
                  "glue:GetJobRun",
                  "glue:GetJobRuns",
                  "glue:GetJobs",
                  "glue:ResetJobBookmark",
                  "glue:StartJobRun",
                  "glue:UpdateJob",
                  "groundtruthlabeling:*",
                  "iam:ListRoles",
                  "kms:DescribeKey",
                  "kms:ListAliases",
                  "lambda:ListFunctions",
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:DescribeLogGroups",
                  "logs:DescribeLogStreams",
                  "logs:GetLogEvents",
                  "logs:PutLogEvents",
                  "sns:ListTopics"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "logs:CreateLogDelivery",
                  "logs:DeleteLogDelivery",
                  "logs:DescribeResourcePolicies",
                  "logs:GetLogDelivery",
                  "logs:ListLogDeliveries",
                  "logs:PutResourcePolicy",
                  "logs:UpdateLogDelivery"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "ecr:SetRepositoryPolicy",
                  "ecr:CompleteLayerUpload",
                  "ecr:BatchDeleteImage",
                  "ecr:UploadLayerPart",
                  "ecr:DeleteRepositoryPolicy",
                  "ecr:InitiateLayerUpload",
                  "ecr:DeleteRepository",
                  "ecr:PutImage"
              ],
              "Resource": "arn:aws:ecr:*:*:repository/*sagemaker*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "codecommit:GitPull",
                  "codecommit:GitPush"
              ],
              "Resource": [
                  "arn:aws:codecommit:*:*:*sagemaker*",
                  "arn:aws:codecommit:*:*:*SageMaker*",
                  "arn:aws:codecommit:*:*:*Sagemaker*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "secretsmanager:ListSecrets"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "secretsmanager:DescribeSecret",
                  "secretsmanager:GetSecretValue",
                  "secretsmanager:CreateSecret"
              ],
              "Resource": [
                  "arn:aws:secretsmanager:*:*:secret:AmazonSageMaker-*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "secretsmanager:DescribeSecret",
                  "secretsmanager:GetSecretValue"
              ],
              "Resource": "*",
              "Condition": {
                  "StringEquals": {
                      "secretsmanager:ResourceTag/SageMaker": "true"
                  }
              }
          },
          {
              "Effect": "Allow",
              "Action": [
                  "robomaker:CreateSimulationApplication",
                  "robomaker:DescribeSimulationApplication",
                  "robomaker:DeleteSimulationApplication"
              ],
              "Resource": [
                  "*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "robomaker:CreateSimulationJob",
                  "robomaker:DescribeSimulationJob",
                  "robomaker:CancelSimulationJob"
              ],
              "Resource": [
                  "*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "s3:GetObject",
                  "s3:PutObject",
                  "s3:DeleteObject"
              ],
              "Resource": [
                  "arn:aws:s3:::*SageMaker*",
                  "arn:aws:s3:::*Sagemaker*",
                  "arn:aws:s3:::*sagemaker*",
                  "arn:aws:s3:::*aws-glue*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "s3:CreateBucket",
                  "s3:GetBucketLocation",
                  "s3:ListBucket",
                  "s3:ListAllMyBuckets"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "s3:GetObject"
              ],
              "Resource": "*",
              "Condition": {
                  "StringEqualsIgnoreCase": {
                      "s3:ExistingObjectTag/SageMaker": "true"
                  }
              }
          },
          {
              "Effect": "Allow",
              "Action": [
                  "lambda:InvokeFunction"
              ],
              "Resource": [
                  "arn:aws:lambda:*:*:function:*SageMaker*",
                  "arn:aws:lambda:*:*:function:*sagemaker*",
                  "arn:aws:lambda:*:*:function:*Sagemaker*",
                  "arn:aws:lambda:*:*:function:*LabelingFunction*"
              ]
          },
          {
              "Action": "iam:CreateServiceLinkedRole",
              "Effect": "Allow",
              "Resource": "arn:aws:iam::*:role/aws-service-role/sagemaker.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_SageMakerEndpoint",
              "Condition": {
                  "StringLike": {
                      "iam:AWSServiceName": "sagemaker.application-autoscaling.amazonaws.com"
                  }
              }
          },
          {
              "Effect": "Allow",
              "Action": "iam:CreateServiceLinkedRole",
              "Resource": "*",
              "Condition": {
                  "StringEquals": {
                      "iam:AWSServiceName": "robomaker.amazonaws.com"
                  }
              }
          },
          {
              "Effect": "Allow",
              "Action": [
                  "sns:Subscribe",
                  "sns:CreateTopic"
              ],
              "Resource": [
                  "arn:aws:sns:*:*:*SageMaker*",
                  "arn:aws:sns:*:*:*Sagemaker*",
                  "arn:aws:sns:*:*:*sagemaker*"
              ]
          },
          {
              "Effect": "Allow",
              "Action": [
                  "iam:PassRole"
              ],
              "Resource": "arn:aws:iam::*:role/*",
              "Condition": {
                  "StringEquals": {
                      "iam:PassedToService": [
                          "sagemaker.amazonaws.com",
                          "glue.amazonaws.com",
                          "robomaker.amazonaws.com"
                      ]
                  }
              }
          }
      ]
  }
  EOF

}

# CloudWatch
resource "aws_cloudwatch_event_rule" "notebook-activity-monitor-trigger" {
  name                = "notebook-activity-monitor-trigger"
  description         = "Stops running notebook instances"
  schedule_expression = "cron(0 21 * * ? *)"
}

resource "aws_cloudwatch_event_target" "target-notebook-activity-monitor-trigger" {
  rule      = "${aws_cloudwatch_event_rule.notebook-activity-monitor-trigger}"
  target_id = "notebook-activity-monitor"
  arn       = "${aws_lambda_function.notebook-activity-monitor.arn}"
}

resource "aws_lambda_permission" "allow-cloudwatch-trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeMethod"
  function_name = "${aws_lambda_function.notebook-activity-monitor.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.notebook-activity-monitor-trigger.arn}"
}