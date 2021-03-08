
# Format error response and append status code.
class DatabaseException(Exception):
    def __init__(self, error):
        print("Exception Raised")
        self.error = error

class BadRequestException(Exception):
    def __init__(self, error):
        print("Exception Raised")
        self.error = error