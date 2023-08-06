import json

from cgdb.resources.stationGroup import StationGroup
from cgdb.utils.ManagerMix import ManagerMix


class StationGroupsManager(ManagerMix):
    def __init__(self, client):
        super(StationGroupsManager, self).__init__(client)

    def station_groups(self):
        content = self.get("station-groups")
        sites = []

        for station_group_raw in content:
            sites.append(StationGroup(**station_group_raw, client=self._client))

        return sites

    def station_group(self, mark):
        content = self.get("station-groups/" + mark)

        return StationGroup(**content, client=self._client)

    def create_station_group(self, code, name=None, description=None):
        out = {"name": name,
               "code": code,
               "description": description}
        result = self.post("station-groups", json.dumps(out))
        if result.status_code != 204:
            raise Exception("upload fail on server side\n Server error:"+result.content.decode("ASCII"))
