from os import environ
from flask import Flask
from bot import FaucyBot

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Faucy Bot!'


@app.route('/stats')
def stats():
    bot = FaucyBot()
    return {
        "safe_list": bot.safe_list,
        "rinkeby": {
            "last_id": bot.get_last_id("rinkeby")
        },
        "goerli": {
            "last_id": bot.get_last_id("goerli")
        },
        "replies": bot.get_replies()
    }


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, host='0.0.0.0', port=environ.get('PORT'))
