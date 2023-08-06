from cgdb.utils.ManagerMix import ManagerMix
from cgdb.resources.parameter import Parameter


class ParametersManager(ManagerMix):
    def __init__(self, client):
        self._client = client


    def parameters(self, path):
        content = self.get(path)
        parameters = []

        for parameters_raw in content:
            parameters.append(Parameter(**parameters_raw, client=self._client))

        return parameters
