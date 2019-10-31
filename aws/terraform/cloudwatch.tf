# Notebook activity monitor
resource "aws_cloudwatch_event_rule" "notebook-activity-monitor-trigger" {
  description         = "Stops running notebook instances"
  is_enabled          = true
  name                = "notebook-activity-monitor-trigger"
  schedule_expression = "cron(0 21 * * ? *)"
  tags                = {}
}

#resource "aws_cloudwatch_event_target" "target-notebook-activity-monitor-trigger" {
#
#}
#
#resource "aws_lambda_permission" "allow-notebook-activity-monitor-trigger" {
#
#}


# Tweet collector
resource "aws_cloudwatch_event_rule" "tweet-collector-trigger" {
  description         = "Triggers tweet-collector function every hour"
  is_enabled          = true
  name                = "tweet-collector-trigger"
  schedule_expression = "cron(0\t0/1\t?\t*\t*\t*)"
  tags                = {}
}

#resource "aws_cloudwatch_event_target" "target-tweet-collector-trigger" {
#
#}
#
#resource "aws_lambda_permission" "allow-tweet-collector-trigger" {
#
#}
