from ledger1.utils.error_client import ClientError

def handle_error(msg, status_code = None):
    raise ClientError(f"Error: {msg}", status_code)
