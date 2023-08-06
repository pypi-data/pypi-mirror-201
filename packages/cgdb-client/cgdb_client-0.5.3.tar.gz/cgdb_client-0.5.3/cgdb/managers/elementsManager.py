import json

from cgdb.resources.element import Element
from cgdb.utils.ManagerMix import ManagerMix


class ElementsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def elements(self, url="elements"):
        content = self.get(url)
        elements = []

        for element_raw in content:
            elements.append(Element(**element_raw, client=self._client))

        return elements

    def element(self, mark):
        content = self.get("elements/" + mark)

        return Element(**content, client=self._client)

    def create_element(self, mark, description, defaultUnit, chartType, defaultColor="#ff0000", categoryId=2):
        out = {"categoryId": categoryId,
                "mark": mark,
                "description": description,
                "defaultUnit": defaultUnit,
                "defaultColor": defaultColor,
                "chartType": chartType}
        result = self.post("elements", json.dumps(out))
        if result.status_code != 200 and result.status_code != 204:
            raise Exception("upload fail on server side\n Server error:"+result.content.decode("ASCII"))

    def set_element_flags(self, element, list_of_flags_names):
        out = []
        for name in list_of_flags_names:
            out.append({"name": name})
        if isinstance(element, str):
            url_element  = "elements/" + element + "/flags"
        else:
            url_element = element.url + "/flags"
        result = self.post(url_element, json.dumps(out))
        if result.status_code != 200 and result.status_code != 204:
            raise Exception("upload fail on server side\n Server error:"+result.content.decode("ASCII"))

    # def add_element_flag(self, element, flag_list_name):
    #     self._client._flag_lists_manager.

    def set_element_parameters(self, element, list_of_parameters_names):
        out = []
        for name in list_of_parameters_names:
            out.append({"name": name})

        result = self.post(element.url+"/parameters", json.dumps(out))
        if result.status_code != 200:
            raise Exception("upload fail on server side\n Server error:"+result.content.decode("ASCII"))

