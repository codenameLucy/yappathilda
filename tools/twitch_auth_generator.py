from multiprocessing import Process

from flask_webserver.flask_main import run_flask
from twitch.tools import get_authentication_code


def initialize_flask_twitch_authentication(twitch_credentials: dict) -> None:
    # Create a thread to run the Flask application
    flask_process = Process(target=run_flask)

    # Start the Flask application in a separate thread to read out redirect parameters
    flask_process.start()

    # initiate authentication
    get_authentication_code(twitch_credentials=twitch_credentials)

    # Wait for the Flask thread to finish
    flask_process.join(5)

    flask_process.kill()
    print(flask_process.is_alive())
