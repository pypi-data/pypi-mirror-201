class Level:
    def __init__(self, id: int, code: str, description: str, level: float):
        self.level = level
        self.description = description
        self.id = id
        self.code = code

    @property
    def url(self):
        if self.code is not None:
            return "levels/" + self.code
        else:
            return "levels/id:" + str(self.id)
