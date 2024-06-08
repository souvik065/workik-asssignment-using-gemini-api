
class FileLimitExceededError(Exception):
    def __init__(self, limit):
        super().__init__(f"File limit of {limit} exceeded.")
        self.limit = limit