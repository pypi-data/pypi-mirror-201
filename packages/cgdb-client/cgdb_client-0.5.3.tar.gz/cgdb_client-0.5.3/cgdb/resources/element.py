class Element:
    def __init__(self, mark: str=None, id: int = None, categoryId: int = None, description: str = None, defaultUnit: str = None, defaultColor: str = None, chartType: str = None, client=None) -> None:
        super().__init__()
        self.mark = mark
        self.id = id
        self.categoryId = categoryId
        self.description = description
        self.defaultUnit = defaultUnit
        self.defaultColor = defaultColor
        self.chartType = chartType

        self._client = client

    @property
    def url(self):
        if self.mark is not None:
            return "elements/" + self.mark
        else:
            return "elements/id:" + str(self.id)

    def data_sets(self):
        return self._client._data_sets_manager.data_sets(self.url)

    def flag_lists(self):
        return self._client._flag_lists_manager.flag_lists(self.url + "/flags")

    def add_flag(self, name):
        current_flag_list_names = [flag.code for flag in self.flag_lists()]

        
