rm tweet-collector.zip
cd lambda
7Z a \tweet-collector.zip *
cd ..
aws lambda update-function-code --function-name tweet-collector --zip-file fileb://tweet-collector.zip
