from cgdb.utils.ManagerMix import ManagerMix
from cgdb.resources.department import Department


class DepartmentsManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def departments(self):
        content = self.get("departments")
        departments = []

        for department_raw in content:
            departments.append(Department(**department_raw, client=self._client))

        return departments

    def department(self, id: str):
        content = self.get("departments/" + id)

        return Department(*content, client=self._client)
