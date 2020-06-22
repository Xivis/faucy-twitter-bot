from os import environ
from flask import Flask
from bot import FaucyBot

app = Flask(__name__)
app.run(host='0.0.0.0', port=environ.get('PORT'))


@app.route('/')
def index():
    return 'Welcome to Facuy Bot!'


@app.route('/stats')
def stats():
    bot = FaucyBot()
    return {
        "safe_list": bot.safe_list,
        "rinkeby": {
            "last_id": bot.get_last_id(bot.networks['rinkeby'])
        },
        "goerli": {
            "last_id": bot.get_last_id(bot.networks['goerli'])
        },
        "replies": bot.get_replies()
    }

