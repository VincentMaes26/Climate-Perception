resource "aws_lambda_function" "notebook-activity-monitor" {
  function_name                  = "notebook-activity-monitor"
  handler                        = "notebook-activity-monitor.lambda_handler"
  layers                         = []
  memory_size                    = 128
  reserved_concurrent_executions = -1
  role                           = "arn:aws:iam::916245739953:role/service-role/notebook-activity-monitor-role-8v4m1pyc"
  source_code_hash               = "${filebase64sha256("../lambda-functions/tweet-collector/lambda/tweet-collector.zip")}"
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
  handler                        = "tweet-collector.lambda_handler"
  layers                         = [
      "arn:aws:lambda:eu-west-1:916245739953:layer:tweepy_layer:2",
      "arn:aws:lambda:eu-west-1:916245739953:layer:pandas25-layer:1",
      "arn:aws:lambda:eu-west-1:399891621064:layer:AWSLambda-Python37-SciPy1x:2"
  ]
  memory_size                    = 128
  reserved_concurrent_executions = -1
  role                           = "arn:aws:iam::916245739953:role/service-role/tweet-collector-role-ucv89lpt"
  source_code_hash               = "${filebase64sha256("../lambda-functions/notebook-monitor/lambda/notebook-activity-monitor.zip")}"
  runtime                        = "python3.7"
  tags                           = {}
  timeout                        = 900



  timeouts {}

  tracing_config {
      mode = "PassThrough"
  }
}
