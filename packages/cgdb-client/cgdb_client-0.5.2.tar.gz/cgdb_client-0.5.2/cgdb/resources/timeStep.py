class TimeStep:
    def __init__(self, id: int, code: str, description: str, codePattern: str, timeStepInterval: dict, timeStepOffset, complex: bool):
        self.codePattern = codePattern
        self.timeStepInterval = timeStepInterval
        self.timeStepOffset = timeStepOffset
        self.complex = complex
        self.description = description
        self.id = id
        self.code = code

    @property
    def url(self):
        if self.code is not None:
            return "time-steps/" + self.code
        else:
            return "time-steps/id:" + str(self.id)
