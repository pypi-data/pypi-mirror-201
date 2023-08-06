from cgdb.resources.stationNetwork import StationNetwork
from cgdb.utils.ManagerMix import ManagerMix

class StationNetworksManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def stationNetworks(self):
        content = self.get("/station-networks")
        station_networks = []

        for station_network_raw in content:
            station_networks.append(StationNetwork(**station_network_raw, client=self._client))

        return station_networks

    def station_network_by_code(self, code):
        content = self.get("station-networks/" + code)

        return StationNetwork(**content, client=self._client)

    def station_network_by_id(self, id):
        content = self.get("station-networks/id:" + str(id))

        return StationNetwork(**content, client=self._client)