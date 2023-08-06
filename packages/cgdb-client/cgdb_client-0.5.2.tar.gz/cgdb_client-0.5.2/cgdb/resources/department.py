class Department:
    def __init__(self, id: str, name: str = None, client=None) -> None:
        super().__init__()
        self.id = id
        self.name = name

        self._client = client
