import logging
import os
import psutil
from subprocess import Popen, CREATE_NEW_CONSOLE
import time

from twitch.tools import get_authentication_code

logger = logging.getLogger(__name__)


class FlaskNotAliveException(Exception):
    pass


def initialize_flask_twitch_authentication(twitch_credentials: dict) -> None:
    # Start the subprocess
    process = Popen(
        f"{os.path.abspath('bottle_main.exe')}",
        shell=True,
        creationflags=CREATE_NEW_CONSOLE,
    )

    time.sleep(5)

    get_authentication_code(twitch_credentials=twitch_credentials)

    time.sleep(5)

    # To terminate the subprocess
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "bottle_main.exe":
            proc.kill()
