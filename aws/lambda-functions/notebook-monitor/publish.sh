cd lambda
rm notebook-activity-monitor.zip
7Z.exe a -r \notebook-activity-monitor.zip *
#aws lambda update-function-code --function-name notebook-activity-monitor --zip-file fileb://notebook-activity-monitor.zip
