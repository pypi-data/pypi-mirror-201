class FromToDateArgumentMissingException(Exception):
    def __init__(self, message="From/To date missing in arguments of function"):
        self.message = message
        super().__init__(self.message)


