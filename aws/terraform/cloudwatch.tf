# Notebook activity monitor
resource "aws_cloudwatch_event_rule" "notebook-activity-monitor-trigger" {

}

resource "aws_cloudwatch_event_target" "target-notebook-activity-monitor-trigger" {

}

resource "aws_lambda_permission" "allow-notebook-activity-monitor-trigger" {

}


# Tweet collector
resource "aws_cloudwatch_event_rule" "tweet-collector-trigger" {

}

resource "aws_cloudwatch_event_target" "target-tweet-collector-trigger" {

}

resource "aws_lambda_permission" "allow-tweet-collector-trigger" {

}
