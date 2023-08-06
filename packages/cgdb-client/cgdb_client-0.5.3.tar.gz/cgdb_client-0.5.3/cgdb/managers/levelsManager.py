import json

from cgdb.resources.level import Level
from cgdb.utils.ManagerMix import ManagerMix


class LevelsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def levels(self):
        content = self.get("levels")
        time_steps = []

        for raw in content:
            time_steps.append(Level(**raw))

        return time_steps

    def level_by_id(self, id):
        content = self.get("levels/id:" + str(id))

        return Level(**content)

    def level_by_code(self, code: str):
        content = self.get("levels/" + str(code))

        return Level(**content)

    def create_level(self, code, description, level):
        out = {"code": code,
                "level": level,
                "description": description}
        result = self.post("levels", json.dumps(out))
        if result.status_code != 200 and result.status_code != 204:
            raise Exception("upload fail on server side\n Server error:"+result.content.decode("ASCII"))

