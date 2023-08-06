class EntityNotFoundException(Exception):
    def __init__(self, code, message="Required entity not found"):
        self.code = code
        self.message = message
        super().__init__(self.message)
