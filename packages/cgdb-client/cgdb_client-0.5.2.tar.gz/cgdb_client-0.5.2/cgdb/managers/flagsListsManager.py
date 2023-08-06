from cgdb.resources.flag import Flag
from cgdb.resources.flagsList import FlagList
from cgdb.utils.ManagerMix import ManagerMix


class FlagListManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def flag_lists(self, path):
        content = self.get(path)
        flags_lists = []

        for flags_list_raw in content:
            flags_list = FlagList(flags_list_raw["id"],
                                        flags_list_raw["name"],
                                        flags_list_raw["description"],
                                        flags = [],
                                        client=self._client)
            for flag_raw in flags_list_raw["flags"]:
                flags_list.flags.append(Flag(**flag_raw))

            flags_lists.append(flags_list)

        return flags_lists
