from cgdb.resources.timeStep import TimeStep
from cgdb.utils.ManagerMix import ManagerMix


class TimeStepsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)


    def time_steps(self):
        content = self.get("time-steps")
        time_steps = []

        for raw in content:
            time_steps.append(TimeStep(**raw))

        return time_steps


    def time_step_by_id(self, id):
        content = self.get("time-steps/id:" + str(id))

        return TimeStep(**content)

    def time_step_by_code(self, code: str):
        content = self.get("time-steps/" + str(code))

        return TimeStep(**content)
