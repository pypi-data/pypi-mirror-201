class StationNetwork:
    def __init__(self, code: str = None, id: int = None, description: int = None, client=None):
        self.id = id
        self.code = code
        self.description = description

        self._client = client

    @property
    def url(self):
        if self.code is not None:
            return "station-networks/" + self.code
        else:
            return "station-networks/id:" + str(self.id)


