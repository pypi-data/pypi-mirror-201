from cgdb.managers.sitesManager import SitesManager

class StationGroup:
    def __init__(self,  id: int = None, code: str = None, name=None, description: int = None, client=None):
        self.id = id
        self.code = code
        self.name = name
        self.description = description

        self._client = client

    @property
    def url(self):
        if self.code is not None:
            return "station-groups/" + self.code
        else:
            return "station-groups/id:" + str(self.id)

    @property
    def sites(self):
        sites_manager = SitesManager(client=self)
        return sites_manager.sites(self.url)
