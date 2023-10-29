import json

from flask import Flask, request

from twitch.tools import get_channel_id

app = Flask("nice")


@app.route('/')
def index():
    # Retrieve query parameters from the URL
    code = request.args.get('code')

    with open("config/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["twitch_credentials"]["code"] = code

    with open("config/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    return "Parameters received, you can close this tab"


def run_flask():
    app.run(host='localhost', port=7000)
