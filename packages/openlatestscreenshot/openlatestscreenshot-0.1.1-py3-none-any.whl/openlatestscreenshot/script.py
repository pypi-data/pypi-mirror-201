from pathlib import Path
import os
import re
from datetime import datetime
import subprocess
from sys import platform


# -----------------
# --- constants ---
# -----------------
DEBUG = False
SUPPORTED_PLATFORMS = ["linux"]
OPEN_COMMANDS = {"linux": "xdg-open"}
REPOSITORY_BUG_REPORT_LINK = (
    "https://gitlab.com/DrTexx/open-latest-screenshot/-/issues"
)
SCREENSHOT_FILENAME_REGEX = (
    r"Screenshot from (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})\.png"
)


# -----------------
# --- functions ---
# -----------------


def ensure_environment_compatible():
    # ensure user is using a supported platform
    if platform not in SUPPORTED_PLATFORMS:
        raise NotImplementedError(
            f"Incompatible platform: {platform} (supported platforms: {','.join(SUPPORTED_PLATFORMS)})"
        )


def open_image_in_default_application(filepath):
    # fetch open command based on platform
    open_command = OPEN_COMMANDS[platform]

    # attempt to open filepath with default image viewer
    try:
        pipes = subprocess.Popen(
            [open_command, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = pipes.communicate()

        # if the process we called had a non-zero return code
        if pipes.returncode != 0:
            # convert stderr byte array to string and strip newline
            err_msg = stderr.decode()
            # raise specific exception with stderr and request user to open new issue
            raise RuntimeError(
                f"Failed to open '{filepath}' with {open_command}, error received:\n  {err_msg}\n\nPlease file a bug report at {REPOSITORY_BUG_REPORT_LINK}"
            )

    # if 'FileNotFoundError' error is raised
    except FileNotFoundError as err:
        # if error is due to platform's open command not being available
        if err.errno == 2 and err.filename == open_command:
            # raise specific error re. platform's open command not being available
            raise NotImplementedError(
                f"Incompatible system: {open_command} is used to open files on your platform ({platform}), however it is not available on your system."
            ) from err
        # if error is due to a different file not being found
        else:
            # raise error normally
            raise err


def open_latest_screenshot():
    ensure_environment_compatible()

    pictures_dirpath = Path("~/Pictures/").expanduser()

    latest_unix_timestamp = 0.0

    # for each path in ~/Pictures
    for filepath in pictures_dirpath.iterdir():
        # if the path is a filepath
        if filepath.is_file():
            # search for a date using the screenshot filename regex
            screenshot_filename = re.search(
                SCREENSHOT_FILENAME_REGEX, filepath.name
            )
            # if the filename matches the screenshot filename regex
            if screenshot_filename is not None:
                # get date from filename as a string
                date_str = screenshot_filename.group(1)
                # convert date string to datetime object
                date = datetime.strptime(date_str, "%Y-%m-%d %H-%M-%S")
                # get datetime as unix timestamp for simple comparison
                unix_timestamp = date.timestamp()
                # if this unix timestamp is more recent than the previously recorded most recent
                if unix_timestamp > latest_unix_timestamp:
                    # record timestamp as the most recent found thus far
                    latest_unix_timestamp = unix_timestamp
                    # record filepath of most recent screenshot found thus far
                    latest_screenshot_filepath = filepath
                    if DEBUG:
                        print(
                            f"{date} is now the most recent screenshot found! ({filepath.name})"
                        )

    if DEBUG:
        print(
            f"{latest_screenshot_filepath} is the most recent of all screenshots searched."
        )

    open_image_in_default_application(latest_screenshot_filepath)
