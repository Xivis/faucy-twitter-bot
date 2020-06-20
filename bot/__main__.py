import os
import time
import tweepy
from dotenv import load_dotenv


class FaucyBot:
    api = None
    loop_time = 10
    users_list_file = 'users_list.txt'
    networks = {
        'goerli': {
            'search_term': '#Goerli #Ethereum',
            'last_tweet_file': 'last_goerli.txt',
            'last_id': 0
        },
        'rinkeby': {
            'search_term': '#Rinkeby #Ethereum',
            'last_tweet_file': 'last_rinkeby.txt',
            'last_id': 0
        }
    }

    safe_list = [
        'faucy3',
        'wewarexivis',
        'gonzalezramiro',
        'lndgalante'
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
            self.networks[key]['last_id'] = self.get_last_id(network)

        # Create users list file if it does not exists
        if not os.path.exists(self.users_list_file):
            with open(self.users_list_file, 'w'):
                pass

    def start(self):
        while True:
            for key, network in self.networks.items():
                new_tweets = self.search(network['search_term'], network['last_id'])
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
                        self.save_last_id(each.id, network)
                        self.networks[key]['last_id'] = each.id
            time.sleep(self.loop_time)

    def get_last_id(self, network):
        try:
            f_read = open(network['last_tweet_file'], 'r')
            last_seen_id = int(f_read.read().strip())
            f_read.close()
        except:
            last_seen_id = self.get_latest_id()
        return last_seen_id

    @staticmethod
    def save_last_id(id, network):
        f_write = open(network['last_tweet_file'], 'w')
        f_write.write(str(id))
        f_write.close()
        return

    def save_user(self, user):
        f_write = open(self.users_list_file, 'a')
        f_write.write(str(user.id)+'\n')
        f_write.close()
        return

    def check_new_user(self, id):
        with open(self.users_list_file) as f:
            datafile = f.readlines()
        for line in datafile:
            if str(id) in line:
                return False
        return True

    def reply_tweet(self, tweet):
        if tweet.user.screen_name in self.safe_list:
            message = 'Hi @{}! Did you try https://faucy.dev ? '.format(
                tweet.user.screen_name
            ) + 'Get all your test $ETH on one site 🚀 🦄'
            self.api.update_status(message, tweet.id)

    def get_latest_id(self):
        """
        Minor hack - As the API does not gives us the latest tweet, we search in our home timeline
        Minor hack2 - Follow an account that tweets every hour :) Thanks @thebigbenclock
        """
        results = self.api.home_timeline()
        for each in results:
            print(each.id, each.created_at, each.text)
        if results:
            return results[0].id
        return 0

    def search(self, query, last_id):
        return self.api.search(query, since_id=last_id)


def main():
    bot = FaucyBot()
    bot.start()


if __name__ == "__main__":
    main()
