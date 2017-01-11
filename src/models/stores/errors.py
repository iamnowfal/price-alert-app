
class StoreException(Exception):
    def __init__(self, message):
        self.message


class StoreNotFoundException(StoreException):
    pass