import os
import json
import time
import tweepy
from dotenv import load_dotenv


class FaucyBot:
    api = None
    loop_time = 150
    db_file = "db.json"
    empty_db = {
      "goerli": 0,
      "rinkeby": 0,
      "users": [],
      "replies": []
    }
    networks = {
        "goerli": {
            "search_term": "#Goerli #Ethereum",
            "last_id": 0
        },
        "rinkeby": {
            "search_term": "#Rinkeby #Ethereum",
            "last_id": 0
        }
    }
    safe_list = [
        "faucy3",
        "wewarexivis",
        "gonzalezramiro",
        "lndgalante"
    ]

    def __init__(self):
        # Load env variables
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        API_SECRET_KEY = os.getenv("API_SECRET_KEY")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

        # Authenticate and create API object
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

        # Load network dictionaries
        for key, network in self.networks.items():
            self.networks[key]["last_id"] = self.get_last_id(key)

        print(">> Faucy Bot Initiated")

    def read_db(self):
        try:
            with open(self.db_file, 'r') as f:
                db = json.load(f)
                return db
        except:
            return self.empty_db

    def write_db(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f)

    def start(self):
        print(">> Faucy Bot Started")
        while True:
            for key, network in self.networks.items():
                new_tweets = self.search(network["search_term"], network["last_id"])
                if new_tweets:
                    # Tweets are ordered by newest first, so we reverse them
                    new_tweets.reverse()
                    for each in new_tweets:
                        # Check if I have responded to user
                        is_new_user = self.check_new_user(each.user.id)
                        if is_new_user:
                            # Reply to user
                            self.reply_tweet(each)
                            self.save_user(each.user)
                        # Save ID
                        self.save_last_id(each.id, key)
                        self.networks[key]["last_id"] = each.id
            time.sleep(self.loop_time)

    def get_last_id(self, network):
        try:
            db = self.read_db()
            last_seen_id = db[network]
        except:
            last_seen_id = self.get_latest_id()
        return last_seen_id

    def save_last_id(self, id, network):
        db = self.read_db()
        db[network] = id
        self.write_db(db)
        return

    def save_user(self, user):
        db = self.read_db()
        db["users"].append(user.id)
        self.write_db(db)
        return

    def save_reply(self, tweet):
        reply = "https://twitter.com/{}/status/{}".format(tweet.user.screen_name, tweet.id)
        db = self.read_db()
        db["replies"].append(reply)
        self.write_db(db)
        return

    def check_new_user(self, id):
        db = self.read_db()
        if id in db["users"]:
            return False
        return True

    def get_replies(self):
        db = self.read_db()
        return db["replies"]

    def reply_tweet(self, tweet):
        if tweet.user.screen_name in self.safe_list:
            message = "Hi @{}! Did you try https://faucy.dev ? ".format(
                tweet.user.screen_name
            ) + "Get all your test $ETH on one site 🚀 🦄"
            try:
                self.api.update_status(message, tweet.id)
            except tweepy.RateLimitError:
                time.sleep(15 * 60)
        self.save_reply(tweet)

    def get_latest_id(self):
        """
        Minor hack - As the API does not gives us the latest tweet, we search in our home timeline
        Minor hack2 - Follow an account that tweets every hour :) Thanks @thebigbenclock
        """
        try:
            results = self.api.home_timeline()
            if results:
                return results[0].id
        except tweepy.RateLimitError:
            pass
        return 0

    def search(self, query, last_id):
        try:
            return self.api.search(query, since_id=last_id)
        except tweepy.RateLimitError:
            pass
        return []


def main():
    bot = FaucyBot()
    bot.start()


if __name__ == "__main__":
    main()
