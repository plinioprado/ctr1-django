class ClientError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code if status_code is not None else 400
        super().__init__(message)
