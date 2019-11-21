data "aws_secretsmanager_secret" "tweepy-credentials" {
  name = "tweet-collector/creds/tweepy"
}
