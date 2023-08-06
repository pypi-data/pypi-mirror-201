class Site:
    def __init__(self, code: str,
                 id: int = None,
                 name: str = None,
                 remark: str = None,
                 gpsLatitude: float = None,
                 gpsLongitude: float = None,
                 altitude: float = None,
                 stationNetworkId = None,
                 client=None,
                 type="STATION",
                 **kwargs):
        self.id = id
        self.name = name
        self.remark = remark
        self.code = code
        self.gpsLatitude = gpsLatitude
        self.gpsLongitude = gpsLongitude
        self.altitude = altitude

        self._client = client

        self.stationNetworkId = stationNetworkId

        self.type = type

    @property
    def url(self):
        if self.code is not None:
            return "sites/" + self.code
        else:
            return "sites/id:" + str(self.id)

    @property
    def stationNetwork(self):
        return self._client._station_networks_manager.stationNetworkById(self.stationNetworkId)

    def data_sets(self):
        return self._client._data_sets_manager.data_sets(self.url, site=self)

    def data_set_by_code(self, element, aggregation, time_step, level=None, elementMarkOverride = None):
        return self._client._data_sets_manager.data_set_by_code(self, element, aggregation, time_step, level, elementMarkOverride)

    def delete_site(self):
        self._client._sites_manager.delete_site(self)
