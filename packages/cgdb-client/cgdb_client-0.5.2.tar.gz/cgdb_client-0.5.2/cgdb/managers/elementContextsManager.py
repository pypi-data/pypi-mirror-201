import json

from cgdb.resources.elementContext import ElementContext
from cgdb.utils.ManagerMix import ManagerMix


class ElementContextsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

        self.elementContextsCached = None

    def element_contexts(self):
        content = self.get("element-contexts")
        element_contexts = []

        for element_context_raw in content:
            element_contexts.append(ElementContext(**element_context_raw, client=self._client))

        return element_contexts

    def element_context(self, id):
        content = self.get("element-contexts/id:" + str(id))

        return ElementContext(**content, client=self._client)

    def element_context_by_element(self, element_mark: str, aggregation: str, timestamp_code: str, level_code:str = None):
        if self.elementContextsCached is None:
            self.elementContextsCached = self.element_contexts()

        for elementContext in self.elementContextsCached:
            code = str(element_mark) + "_" + aggregation + "_" + str(timestamp_code)
            if level_code is not None:
                code += "_" + str(level_code)
            # if elementContext.aggregation == aggregation and elementContext.element.mark == element_mark and elementContext.time_step.code == timestamp_code and (level_code is None or (level_code is not None and elementContext.levelId is not None and elementContext.level.code == level_code)):
            #     return elementContext
            if elementContext.code == code:
                return elementContext

        return None
    
    def create_element_context(self, element, aggregation, timeStep, level=None):
        content = {"elementId": element.id,
                   "timeStepId": timeStep.id,
                   "aggregation": aggregation}

        if level is not None:
            content["levelId"] = level.id

        self.post('element-contexts', json.dumps(content))
        self.elementContextsCached = self.element_contexts()
