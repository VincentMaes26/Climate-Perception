cd lambda
rm tweet-etl.zip
7Z.exe a -r \tweet-etl.zip *
#aws lambda update-function-code --function-name tweet-etl --zip-file fileb://tweet-etl.zip
