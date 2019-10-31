resource "aws_lambda_function" "notebook-activity-monitor" {
  function_name                  = "notebook-activity-monitor"
  handler                        = "lambda_function.lambda_handler"
  layers                         = []
  memory_size                    = 128
  reserved_concurrent_executions = -1
  role                           = "arn:aws:iam::916245739953:role/service-role/notebook-activity-monitor-role-8v4m1pyc"
  runtime                        = "python3.6"
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
  id                             = "tweet-collector"
  last_modified                  = "2019-10-24T10:09:03.918+0000"
  layers                         = [
      "arn:aws:lambda:eu-west-1:916245739953:layer:tweepy_layer:2",
      "arn:aws:lambda:eu-west-1:113088814899:layer:Klayers-python37-pandas:1",
  ]
  memory_size                    = 128
  reserved_concurrent_executions = -1
  role                           = "arn:aws:iam::916245739953:role/service-role/tweet_scraper-role-lzcqklfa"
  runtime                        = "python3.7"
  tags                           = {}
  timeout                        = 900

  environment {
      variables = {
          "tweepy_ACCESS_SECRET"   = "YIGI7drHS0WeehJtB60JjWxLFjzPTJ9fkbp7zZbxA0CHa"
          "tweepy_ACCESS_TOKEN"    = "434059213-ZThQOr6nxAMMiV8RImlqIO4rmgtcIlWiAOrOf4JQ"
          "tweepy_CONSUMER_KEY"    = "AbleQFvj6SsbFc7RtmUQTMR36"
          "tweepy_CONSUMER_SECRET" = "PBEw2PtmbeMyJ6hpmPI17jghZoB7jOvBdhtaDEhbhfbMZb6klj"
      }
  }

  timeouts {}

  tracing_config {
      mode = "PassThrough"
  }
}
