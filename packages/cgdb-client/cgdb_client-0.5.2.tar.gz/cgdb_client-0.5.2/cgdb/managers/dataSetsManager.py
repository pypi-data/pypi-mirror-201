from datetime import datetime
import json
import pytz

import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from cgdb.exceptions.ColumnNotFound import ColumnNotFoundException
from cgdb.resources import OverwriteStrategy
from cgdb.resources.dataSet import DataSet
from cgdb.utils.ManagerMix import ManagerMix


def _json_values_to_dataframe(values, mapping_flags, mapping_params, data_set: DataSet):
    records = []
    for record in values:
        record_to_data_frame = {"timestamp": record["timestamp"], "value": record["value"]}
        if record["flags"] is not None:
            for flag in record["flags"]:
                flag_info = mapping_flags[flag]
                record_to_data_frame[flag_info[0]] = flag_info[1]
        if record["parameters"] is not None:
            for param_col, param_value in record["parameters"].items():
                param_info = mapping_params[param_col]
                record_to_data_frame[param_info[0]] = param_value

        records.append(record_to_data_frame)

    if len(records) == 0:
        return pd.DataFrame({"datetime": [], "value": []})

    data_page = pd.DataFrame(records)
    data_page["timestamp"] = data_page["timestamp"]+7200
    data_page["timestamp"] = pd.to_datetime(data_page['timestamp'], unit="s", )
    # data_page.timestamp = data_page.timestamp.dt.tz_localize('Europe/Brussels')
    data_page.rename(columns={"timestamp": "datetime", "value": data_set.code}, inplace=True)
    for parameter in data_set.parameters:
        if parameter.name in data_page.columns and parameter.type in ["INTEGER", "DOUBLE"]:
            data_page[parameter.name] = pd.to_numeric(data_page[parameter.name])

    return data_page


class DataSetsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def data_sets(self, url=None, site=None):
        content = self.get(url + "/data-sets")
        data_sets = []

        for station_raw in content:
            data_sets.append(DataSet(**station_raw, client=self._client, site=site))

        return data_sets

    def data_set_by_code(self, site, element, aggregation, time_step, level=None, elementMarkOverride=None):
        if elementMarkOverride is not None:
            element = elementMarkOverride
        code = element + "_" + aggregation + "_" + str(time_step)
        if level is not None:
            code += "_" + str(level)
        content = self.get(site.url + "/data-sets/" + code)

        return DataSet(**content, client=self._client, site=site)

    # def get_data_set_data(self, data_set: DataSet, date_from: datetime.datetime = None, date_to: datetime.datetime = None):
    #     if (date_from is not None and date_to is None) or (date_from is None and date_to is not None):
    #         print("one date missing")
    #         return
    #
    #     url = f"{data_set.url}/data"
    #
    #     if date_from is not None and date_to is not None:
    #         date_from = int(date_from.timestamp())
    #         date_to = int(date_to.timestamp())
    #
    #         url_param = f"?date-time-from={date_from}&date-time-to={date_to}&page-size=500"
    #         url += url_param
    #
    #
    #     content = self.get(url)
    #     items_count = content["itemsCount"]
    #     items_count_loaded = 0
    #     page = 0
    #     data=None
    #     # load data from pages
    #     while items_count_loaded < items_count:
    #         if items_count_loaded == 0:
    #             values = content["values"]
    #         else:
    #             values = self.get(url+"&page="+str(items_count_loaded))["values"]
    #
    #         mapping_flags = data_set._mapping_flags_to_value()
    #         mapping_params = data_set._mapping_parameters_to_col_name_type()
    #
    #         items_count_loaded += len(values)
    #         page += 1
    #         records = []
    #         for record in values:
    #             record_to_data_frame = {"timestamp": record["timestamp"], "value": record["value"]}
    #             if record["flags"] is not None:
    #                 for flag in record["flags"]:
    #                     flag_info = mapping_flags[flag]
    #                     record_to_data_frame[flag_info[0]] = flag_info[1]
    #             if record["parameters"] is not None:
    #                 for param_col, param_value in record["parameters"].items():
    #                     param_info = mapping_params[param_col]
    #                     record_to_data_frame[param_info[0]] = param_value
    #
    #             records.append(record_to_data_frame)
    #
    #         if data is None and len(records) == 0:
    #             return pd.DataFrame({"datetime": [], "value":[]})
    #
    #         data_page = pd.DataFrame(records)
    #         data_page["timestamp"] = pd.to_datetime(data_page['timestamp'], unit="s")
    #         # data_page.timestamp = data_page.timestamp.dt.tz_localize('UTC').dt.tz_convert('Europe/Brussels')
    #         data_page.rename(columns={"timestamp": "datetime", "value": data_set.code}, inplace=True)
    #         for parameter in data_set.parameters:
    #             if parameter.name in data_page.columns and parameter.type in ["INTEGER", "DOUBLE"]:
    #                 data_page[parameter.name] = pd.to_numeric(data_page[parameter.name])
    #
    #         if data is None:
    #             data = data_page
    #         else:
    #             data = pd.concat([data, data_page])
    #
    #     return data

    def get_data_set_data2(self, data_set: DataSet, date_from: str = None, date_to: str = None):
        if (date_from is not None and date_to is None) or (date_from is None and date_to is not None):
            print("one date missing")
            return

        url = f"{data_set.url}/data"

        if date_from is not None and date_to is not None:
            date_from = int(datetime
                            .strptime(date_from, "%Y-%m-%d %H:%M")
                            .replace(tzinfo=pytz.timezone("UTC")).timestamp()) - 3600*2
            # date_from = date_from - (date_from % 300)
            date_to = int(datetime
                          .strptime(date_to, "%Y-%m-%d %H:%M")
                          .replace(tzinfo=pytz.timezone("UTC")).timestamp()) - 3600*2
            # date_to = date_to - (date_to % 300)

            url_param = f"?date-time-from={date_from}&page-size=10000"
            url += url_param

        content = self.get(url + f"&date-time-to={date_to}")
        print(url + f"&date-time-to={date_to}")
        values = content["values"]
        items_count = content["itemsCount"]
        print("items count:" + str(items_count))

        mapping_flags = data_set._mapping_flags_to_value()
        mapping_params = data_set._mapping_parameters_to_col_name_type()

        data = _json_values_to_dataframe(values, mapping_flags, mapping_params, data_set)

        items_count_loaded = data.shape[0]
        items_count_loaded_left = items_count - items_count_loaded

        while items_count_loaded_left > 0:
            date_to = values[-1]["timestamp"] - 1

            content = self.get(url + f"&date-time-to={date_to}")
            print(url + f"&date-time-to={date_to}")
            print("items count:" + str(content["itemsCount"]))
            values = content["values"]

            data_tmp = _json_values_to_dataframe(values, mapping_flags, mapping_params, data_set)
            items_count_loaded = data_tmp.shape[0]
            items_count_loaded_left = items_count_loaded_left - items_count_loaded

            data = pd.concat([data, data_tmp])

        # data['datetime'] = data['datetime'].dt.tz_localize('utc').dt.tz_convert("Europe/Prague")

        return data

    # def make_empty_data_frame(self,data_set):
    #     columns = {"timestamp": pd.Series(dtype="int"),
    #                "value": pd.Series(dtype="float")}
    #
    #     for flags_list in data_set.flags:
    #         columns[flags_list.name] = pd.Series(dtype="str")
    #
    #     for parameter in data_set.parameters:
    #         columns[parameter.name] = pd.Series(dtype="str")
    #
    #     return pd.DataFrame(columns)

    def post_data_set_data2(self, data: pd.DataFrame, data_set: DataSet, overwriteStrategy: str = None):
        print(data)

        if "date_time" not in data.columns:
            raise ColumnNotFoundException("date_time")
        elif "value" not in data.columns:
            raise ColumnNotFoundException("value")

        data = data.dropna(subset=["value"])

        parameters_prefix_columns_data = [column_name for column_name in data.columns if
                                          column_name.startswith("parameter-")]
        flags_prefix_columns_data = [column_name for column_name in data.columns if column_name.startswith("flag-")]

        data_set_parameters_names = [parameter.name for parameter in data_set.parameters]
        data_set_flags_names = [flag.name for flag in data_set.flags]

        if not all(column in data_set_parameters_names for column in
                   [column_with_prefix[len("parameter-"):] for column_with_prefix in parameters_prefix_columns_data]):
            raise Exception("parameters columns are not in data set. columns: " + str(
                parameters_prefix_columns_data) + " in data set: " + str(data_set_parameters_names))
        if not all(column in data_set_flags_names for column in
                   [column_with_prefix[len("flag-"):] for column_with_prefix in flags_prefix_columns_data]):
            raise Exception("flags columns are not in data set. columns: " + str(
                flags_prefix_columns_data) + " in data set: " + str(data_set_flags_names))

        data = data[["date_time", "value"] + parameters_prefix_columns_data + flags_prefix_columns_data].copy()

        flags_mapping = data_set._mapping_flags_values_to_id()
        parameters_mapping = data_set._mapping_parameters_col_to_id_type()

        for flag_column_data in flags_prefix_columns_data:
            data[flag_column_data] = data[flag_column_data].map(flags_mapping[flag_column_data])

        parameters_id_columns_data = []
        for parameter_column_data in parameters_prefix_columns_data:
            if parameters_mapping[parameter_column_data][1] == "INTEGER":
                try:
                    data[parameter_column_data] = data[parameter_column_data].astype('Int64')
                except TypeError:
                    raise Exception("Paramater column:" + parameter_column_data + " must be integer")
            elif parameters_mapping[parameter_column_data][1] == "DOUBLE" and data.dtypes[
                parameter_column_data] != np.float64:
                raise Exception("Paramater column:" + parameter_column_data + " must be Double")
            data.rename(columns={parameter_column_data: str(parameters_mapping[parameter_column_data][0])},
                        inplace=True)
            parameters_id_columns_data.append(str(parameters_mapping[parameter_column_data][0]))

        if is_datetime(data["date_time"]):
            data['date_time'] = data.date_time.dt.tz_localize(tz="UTC")
            data["date_time"] = (data.date_time.values.astype(np.int64) / 10 ** 9).astype(np.int64) - 7200

        out = []
        for index, row in data.iterrows():
            if len(flags_prefix_columns_data) == 0:
                flags = None
            else:
                flags = []
                for col in flags_prefix_columns_data:
                    if not pd.isnull(row[col]):
                        flags.append(int(row[col]))

            if len(parameters_id_columns_data) == 0:
                parameters = None
            else:
                parameters = {}
                for col in parameters_id_columns_data:
                    if not pd.isnull(row[col]):
                        parameters[col] = str(row[col])

            out.append({"timestamp": int(row["date_time"]), "value": float(row["value"]), "parameters": parameters,
                        "flags": flags})

        out = json.dumps(out)

        url = data_set.url + "/data"

        if overwriteStrategy is not None:
            url += "?overwriteStrategy=" + overwriteStrategy

        a = self._client._session.post(url, data=out)
        if a.status_code != 200:
            raise Exception("upload fail on server side " + a.text)

    # def post_data_set_data(self, url, data: pd.DataFrame, date_time_column_name:str = "date_time", value_column_name:str = "value", parameter_columns_names:dict = None, flags_columns_names:dict = None, flags=None, parameters=None):
    #     url = f"{url}/data"
    #
    #     if date_time_column_name not in data.columns:
    #         raise ColumnNotFoundException(date_time_column_name)
    #     elif value_column_name not in data.columns:
    #         raise ColumnNotFoundException(value_column_name)
    #     elif not parameters is not None and set(parameter_columns_names.values()).issubset(data.columns):
    #         raise ColumnNotFoundException(','.join([column_name for parameter_name, column_name in parameter_columns_names]))
    #
    #     rename_dict, columns = self._rename_column_dict(date_time_column_name, value_column_name, parameter_columns_names, flags_columns_names)
    #
    #     out = data[columns].copy().dropna()
    #     # content = out.to_json(orient="records")
    #     content = self._prepare_json(out,rename_dict,parameter_columns_names, flags_columns_names, flags=flags, parameters=parameters)
    #
    #     a = self._client._session.post(url, data=content)
    #     if a.status_code != 200:
    #         raise Exception("upload fail")
    #     print(a)
    #
    # def _rename_column_dict(self, date_time_column_name: str, value_column_name: str, parameter_columns_names: dict, flags_columns_names: dict):
    #     out_dict = {date_time_column_name: "timestamp",
    #            value_column_name: "value"}
    #     out_list = [date_time_column_name, value_column_name]
    #
    #     if parameter_columns_names is not None:
    #         for parameter, column_name in parameter_columns_names.items():
    #             out_dict[column_name] = "parameter-" + parameter
    #             out_list.append(column_name)
    #
    #     if flags_columns_names is not None:
    #         for flag, column_name in flags_columns_names.items():
    #             out_dict[column_name] = "flag-" + flag
    #             out_list.append(column_name)
    #
    #     return out_dict, out_list
    #
    # def _prepare_json(self, data, rename_param, parameters_maping, flags_maping, flags, parameters):
    #     data = data.rename(columns=rename_param)
    #     data["timestamp"] = (data.timestamp.values.astype(np.int64) / 10**9) - 3600
    #
    #     parameters_actual = {}
    #     flags_actual = {}
    #     flags_value_maping = {}
    #
    #     if parameters_maping is not None:
    #         for parameter_name in parameters_maping:
    #             for parameters_all_one in parameters:
    #                 if parameters_all_one.name == parameter_name:
    #                     parameters_actual["parameter-"+parameter_name] = parameters_all_one.id
    #
    #     if parameters_maping is not None:
    #         for flag_list_name in flags_maping:
    #             for flags_all_one in flags:
    #                 if flags_all_one.name == flag_list_name:
    #                     flags_actual["flag-"+flag_list_name] = flags_all_one.id
    #                     flags_value_maping["flag-"+flag_list_name] = {}
    #                     for flag in flags_all_one.flags:
    #                         flags_value_maping["flag-"+flag_list_name][flag.code] = flag.id
    #
    #         data.replace(flags_value_maping, inplace=True)
    #     out = []
    #
    #     for index, row in data.iterrows():
    #         if len(parameters_actual.keys()) == 0:
    #             parameters = None
    #         else:
    #             parameters = {}
    #             for param in parameters_actual:
    #                 parameters[str(parameters_actual[param])] = str(int(row[param]))
    #
    #         if len(flags_actual.keys()) == 0:
    #             flags = None
    #         else:
    #             flags = []
    #             for flag in flags_actual:
    #                 flags.append(int(row[flag]))
    #
    #         out.append({"timestamp": int(row["timestamp"]), "value": float(row["value"]), "parameters": parameters, "flags": flags})
    #
    #     return json.dumps(out)

    def create_data_set(self, station, element_code, aggregation, time_step_code, level_code, data_set_type="TECHNICAL",
                        elementMarkOverride=None, description=None):
        element_context = self._client._element_contexts_manager.element_context_by_element(element_code, aggregation,
                                                                                            time_step_code, level_code)

        url = station.url + "/data-sets"

        content = {"contextId": element_context.id,
                   "elementMarkOverride": elementMarkOverride,
                   "dataSetType": data_set_type,
                   "description": description}

        self.post(url, json.dumps(content))

    def delete_data_set(self, data_set: DataSet):
        self.delete(data_set.url)
