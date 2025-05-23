from datetime import datetime
from ctr1.utils.error_client import ClientError
from ctr1.utils import fileio


def handle_error(msg, status_code = None):
    error_msg = f"Error: {msg}"
    now = datetime.now()

    fileio.add_text(
        "./ctr1/file/error.log",
        f"{now.strftime("%Y-%m-%d %H:%M:%S")} {error_msg}")

    raise ClientError(error_msg, status_code)


def log_error(msg):
    error_msg = f"Error: {msg}"
    now = datetime.now()

    fileio.add_text(
        "./ctr1/file/error.log",
        f"{now.strftime("%Y-%m-%d %H:%M:%S")} {error_msg}")
