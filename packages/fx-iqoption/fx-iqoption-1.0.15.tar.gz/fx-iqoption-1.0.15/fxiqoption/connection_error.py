class ConnectionError(Exception):

    def __init__(self, message="Lost connection. Try to login again"):
        self.message = message
        super().__init__(self.message)