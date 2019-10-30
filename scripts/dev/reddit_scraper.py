import json
import praw

# Gets authentication details from json file and connects to API
def conntect_to_API():

    with open("../credentials/reddit_credentials.json", "r") as file:
        creds = json.load(file)

    try:
        reddit = praw.Reddit(client_id = creds["CLIENT_ID"],
                            client_secret = creds["CLIENT_SECRET"],
                            password = creds["PASSWORD"],
                            user_agent=creds["USER_AGENT"],
                            username=creds["USERNAME"])
        print("Connected as user: " + str(reddit.user.me()))
        return reddit  

    except KeyError as keyError:
        print("Something went wrong. KeyError:" + str(keyError))

    except Exception as ex:
        print("Something went wrong. Error:"+ str(ex))

def get_post():
    reddit = conntect_to_API()
    posts = reddit.subreddit('environment').new(limit=20)
    #print(dir(test))
    #print(len(list(posts)))
    [print("Title: {0}\nBody: {1}\n\n\n".format(post.title, post.selftext)) for post in posts]

if __name__ == "__main__":
    get_post()
