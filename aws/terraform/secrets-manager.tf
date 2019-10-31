data "aws_secretsmanager_secret" "tweepy-credentials" {
  name = "tweet-collector/tweepy/credentials" 
}
