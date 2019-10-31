# tweet collector
resource "aws_lambda_layer_version" "tweepy_layer" {
  compatible_runtimes = [
      "python3.6",
      "python3.7",
  ]
  id                  = "arn:aws:lambda:eu-west-1:916245739953:layer:tweepy_layer:2"
  layer_name          = "tweepy_layer"
  source_code_hash    = "6N1KQipdh625mkHkk+D/HBYHL22Qd4WObgF2hlYHNLY="
  version             = "2"
}

resource "aws_lambda_layer_version" "pandas25-layer" {
  compatible_runtimes = [
      "python3.7",
  ]
  id                  = "arn:aws:lambda:eu-west-1:916245739953:layer:pandas25-layer:1"
  layer_name          = "pandas25-layer"
  source_code_hash    = "HDnMXUK9iz8zA6800z5ziLp2UR+KwXUv7HwK4WsOzp0="
  version             = "1"
}
