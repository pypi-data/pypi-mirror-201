import json

from cgdb.resources.site import Site
from cgdb.utils.ManagerMix import ManagerMix


class SitesManager(ManagerMix):
    def __init__(self, client):
        super(SitesManager, self).__init__(client)

    def sites(self, url="sites"):
        content = self.get(url)
        sites = []

        for station_raw in content:
            sites.append(Site(**station_raw, client=self._client))

        return sites

    def site(self, mark):
        content = self.get("sites/" + mark)

        return Site(**content, client=self._client)

    def create_station(self, name, code, gpsLatitude, gpsLongitude, altitude, stationNetworkCode, stationGroupCode=None, remark=""):
        station_network = self._client._station_networks_manager.station_network_by_code(stationNetworkCode)
        out = {"name": name,
               "remark": remark,
               "code": code,
               "gpsLatitude": gpsLatitude,
               "gpsLongitude": gpsLongitude,
               "altitude": altitude,
               "stationNetworkId": station_network.id}
        if stationGroupCode is not None:
            station_group = self._client.station_group(stationGroupCode)
            out["stationGroupId"] = station_group.id

        result = self.post("sites", json.dumps(out))
        if result.status_code != 200:
            raise Exception("upload fail on server side\n Server error:"+result.content.decode("ASCII"))

    def delete_site(self, site: Site):
        self.delete(site.url)
