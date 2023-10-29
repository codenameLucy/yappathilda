import json
import logging

from bottle import route, run, request

logger = logging.getLogger(__name__)


@route('/')
def index():
    # Retrieve query parameters from the URL
    code = request.query.get('code')

    with open(f"config/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["twitch_credentials"]["code"] = code

    with open("config/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    return "Parameters received, you can close this tab"


def run_bottle():
    try:
        run(host='localhost', port=7000)
        logger.info("This message shouldn't be visible.. what happened?")
    except Exception as e:
        logger.critical(f"An error occurred during init of flask: {str(e)}")


if __name__ == "__main__":
    run_bottle()