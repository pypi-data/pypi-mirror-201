class ElementsCategory:
    def __init__(self, code: str, id: int = None, description: str = None, client=None):
        self.code = code
        self.id = id
        self.description = description

        self._client = client

    @property
    def url(self):
        return "/elements-categories/" + self.code

    def elements(self):
        self._client._elements_manager.elements(self.url + "/elements")
