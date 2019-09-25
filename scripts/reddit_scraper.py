import json
import praw

# Gets authentication details from json file and connects to API
def conntect_to_API():
    with open("../credentials/reddit_credentials.json", "r") as file:
        creds = json.load(file)

    reddit = praw.Reddit(client_id = creds["CLIENT_ID"],
                        client_secret = creds["CLIENT_SECRET"],
                        password = creds["PASSWORD"],
                        user_agent=creds["USER_AGENT"],
                        username=creds["USERNAME"])
    return reddit


# Prints out error message 
def test_connection():
    try:
        reddit = conntect_to_API()
        print("Connected as user: " + reddit.user.me())
    except KeyError as keyError:
        print("Something went wrong. KeyError:" + str(keyError))
    except Exception as ex:
        print("Something went wrong. Error:"+ str(ex))

if __name__ == "__main__":
    test_connection()