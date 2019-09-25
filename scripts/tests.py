import datetime
import progressbar as pb
import json

if __name__ == "__main__":
    today = datetime.date.today()
    print(today)

    with open("../credentials/twitter_credentials.json", "r") as file:
        creds = json.load(file)
        print(creds)

   