pip install -r requirements.txt -t python/ --upgrade
zip -q -r tweepy_layer.zip . -x "test*" -x "*__pycache__*" -x "build.sh"