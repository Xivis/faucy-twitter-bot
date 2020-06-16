import os
import tweepy
from dotenv import load_dotenv


class FaucyBot:
    api = None
    last_id = 1272572630764150785

    def __init__(self):
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        API_SECRET_KEY = os.getenv("API_SECRET_KEY")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = tweepy.API(auth)

        # TODO - Get last status ID

    def save_last_id(self, id, network):
        # TODO - Save last status ID found
        pass

    def save_user(self, network):
        # TODO - Save user that received a reply (to not tweet them again)
        pass

    def reply_tweet(self, tweet,):
        message = 'Hi @{}! Did you try https://faucy.dev? '.format(
            tweet.user.screen_name
        ) + 'Get all your test $ETH on one site 🚀 🦄'
        self.api.update_status(message, tweet.id)

    def search(self, query):
        results = self.api.search(query, since_id=self.last_id)
        for each in results:
            print(each.id, ' - ', each.user.screen_name, ' - ', each.text)

def main():
    bot = FaucyBot()
    bot.search('#Rinkeby #Ethereum')

if __name__ == "__main__":
    main()
