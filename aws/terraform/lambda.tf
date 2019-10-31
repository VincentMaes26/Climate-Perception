resource "aws_lambda_function" "notebook-activity-monitor" {
  function_name                  = "notebook-activity-monitor"
  handler                        = "lambda_function.lambda_handler"
  layers                         = []
  memory_size                    = 128
  reserved_concurrent_executions = -1
  role                           = "arn:aws:iam::916245739953:role/service-role/notebook-activity-monitor-role-8v4m1pyc"
  runtime                        = "python3.7"
  tags                           = {}
  timeout                        = 3

  timeouts {}

  tracing_config {
      mode = "PassThrough"
  }
}

resource "aws_lambda_function" "tweet-collector" {
  function_name                  = "tweet-collector"
  handler                        = "lambda_function.lambda_handler"
  layers                         = [
      "arn:aws:lambda:eu-west-1:916245739953:layer:tweepy_layer:2",
      "arn:aws:lambda:eu-west-1:916245739953:layer:pandas25-layer:1",
      "arn:aws:lambda:eu-west-1:399891621064:layer:AWSLambda-Python37-SciPy1x:2"
  ]
  memory_size                    = 128
  reserved_concurrent_executions = -1
  role                           = "arn:aws:iam::916245739953:role/service-role/tweet_scraper-role-lzcqklfa"
  runtime                        = "python3.7"
  tags                           = {}
  timeout                        = 900



  timeouts {}

  tracing_config {
      mode = "PassThrough"
  }
}
