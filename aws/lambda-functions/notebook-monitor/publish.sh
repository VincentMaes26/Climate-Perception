rm notebook-activity-monitor.zip
cd lambda
7Z a \notebook-activity-monitor.zip *
cd ..
aws lambda update-function-code --function-name notebook-activity-monitor --zip-file fileb://notebook-activity-monitor.zip
