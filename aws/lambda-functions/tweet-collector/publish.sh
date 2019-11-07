cd lambda
rm tweet-collector.zip
7Z.exe a -r \tweet-collector.zip *
aws lambda update-function-code --function-name tweet-collector --zip-file fileb://tweet-collector.zip
