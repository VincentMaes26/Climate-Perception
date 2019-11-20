# tweet collector
resource "aws_lambda_layer_version" "tweepy_layer" {
  compatible_runtimes = [
    "python3.6",
    "python3.7",
  ]
  layer_name       = "tweepy_layer"
  source_code_hash = "6N1KQipdh625mkHkk+D/HBYHL22Qd4WObgF2hlYHNLY="
}

resource "aws_lambda_layer_version" "pandas25-layer" {
  compatible_runtimes = [
    "python3.7",
  ]
  layer_name       = "pandas25-layer"
  source_code_hash = "HDnMXUK9iz8zA6800z5ziLp2UR+KwXUv7HwK4WsOzp0="
}

resource "aws_lambda_layer_version" "nltk-layer" {
  compatible_runtimes = [
    "python3.7",
  ]
  layer_name       = "nltk-layer"
  filename         = "../aws-nltk-layer/nltk-layer.zip"
  source_code_hash = "${filebase64sha256("../aws-nltk-layer/nltk-layer.zip")}"
}
