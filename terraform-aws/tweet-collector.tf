# Lambda function 
resource "aws_lambda_function" "tweet-collector" {
  function_name = "tweet-collector"
  handler = "lambda_function.lambda_handler"
  runtime = "Python 3.7"
  role = "${aws_iam_role.tweet-collector-role}"

  layers = [
    "${aws_lambda_layer_version.tweepy_layer}",
    "${aws_lambda_layer_version.Klayers-python37-pandas}"
  ]

  environment {
    variables = {
      tweepy_ACCESS_SECRET = "${var.tweepy_ACCESS_SECRET}"
      tweepy_ACCESS_TOKEN = "${var.tweepy_ACCESS_TOKEN}"
      tweepy_CONSUMER_KEY = "${var.tweepy_CONSUMER_KEY}"
      tweepy_CONSUMER_SECRET = "${var.tweepy_CONSUMER_SECRET}"
    }
  }
}


# Role
resource "aws_iam_role" "tweet-collector-role" {
  
}

# Lambda layers
resource "aws_lambda_layer_version" "tweepy_layer" {
  
}

resource "aws_lambda_layer_version" "pandas25-layer" {
  
}

# Cloudwatch 
resource "aws_cloudwatch_event_rule" "tweet-collector-trigger" {
  name = "tweet-collector-trigger"
  description = "Runs tweet-collector every hour"
  schedule_expression = "cron(0 0/1 ? * * *)"
}

resource "aws_cloudwatch_event_target" "target-tweet-collector-trigger" {
  rule = "${aws_cloudwatch_event_rule.tweet-collector-trigger}"
  target_id = "tweet-collector"
  arn = "${aws_lambda_function.tweet-collector.arn}"
}

resource "aws_lambda_permission" "allow-cloudwatch-trigger" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeMethod"
  function_name = "${aws_lambda_function.tweet-collector.function_name}"
  principal = "events.amazonaws.com"
  source_arn = "${aws_cloudwatch_event_rule.tweet-collector-trigger.arn}"
}

