"""
.. include:: ./dataSet.md
"""
from datetime import datetime

import pandas as pd


class DataSet:

    def __init__(self, code: str, siteId: int = None, id: int = None, elementId: int = None, contextId: int = None, description: str = None,
                 elementMarkOverride=None, dataSetType: str = None, client=None, site=None):
        super().__init__()

        self.site = site
        self._client = client
        self.code = code

        self.elementId = elementId

        self.description = description
        self.element = self._client.element("id:"+str(self.elementId))
        self.id = id
        self.siteId = siteId
        self.contextId = contextId
        self.elementMarkOverride = elementMarkOverride
        self.dataSetType = dataSetType

    @property
    def url(self):
        return self.site.url + "/data-sets/" + self.code

    @property
    def flags(self):
        return self.element.flag_lists()

    @property
    def parameters(self):
        return self._client._parameters_manager.parameters(str(self.element.url) + "/parameters")

    def data(self, date_from: datetime = None, date_to: datetime = None):
        return self._client._data_sets_manager.get_data_set_data2(self, date_from, date_to)

    def post_data(self, data: pd.DataFrame, overwriteStrategy:str = None):
        return self._client._data_sets_manager.post_data_set_data2(data, self, overwriteStrategy)

    def delete_data_set(self):
        return self._client._data_sets_manager.delete_data_set(self)

    def _mapping_flags_to_value(self):
        flags_lists = self.flags
        mapping = {}
        for flags_list in flags_lists:
            for flag in flags_list.flags:
                mapping[flag.id] = (flags_list.name, flag.code)
        return mapping

    def _mapping_parameters_to_col_name_type(self):
        parameters = self.parameters
        mapping = {}
        for parameter in parameters:
            mapping[str(parameter.id)] = (parameter.name, parameter.type)
        return mapping

    def _mapping_flags_values_to_id(self):
        flags_lists = self.flags
        mapping_lists = {}
        for flags_list in flags_lists:
            mapping_list = {}
            for flag in flags_list.flags:
                mapping_list[flag.code] = flag.id
            mapping_lists["flag-" + flags_list.name] = mapping_list
        return mapping_lists
    
    def _mapping_parameters_col_to_id_type(self):
        parameters = self.parameters
        mapping = {}
        for parameter in parameters:
            mapping["parameter-"+str(parameter.name)] = (parameter.id, parameter.type)
        return mapping
