class ElementContext:
    def __init__(self, id: int, elementId: int = None, timeStepId: int = None, code: str = None, aggregation: str = None, unit: str = None, levelId: int = None, client=None):
        self.unit = unit
        self.aggregation = aggregation
        self.levelId = levelId
        self.timeStepId = timeStepId
        self.elementId = elementId
        self.code = code
        self.id = id

        self._client = client

        self.__load_element()
        self.__load_time_step()
        if self.code.count("_") == 3:
            self.__load_level()
        else:
            self.level = None


    @property
    def url(self):
        return "/element-contexts/id:" + str(self.id)

    def __load_element(self):
        self.element = self._client._elements_manager.element("id:"+str(self.elementId))

    def __load_time_step(self):
        self.time_step = self._client._time_steps_manager.time_step_by_id(self.timeStepId)

    def __load_level(self):
        if self.levelId is not None:
            self.level = self._client._levels_manager.level_by_id(self.levelId)