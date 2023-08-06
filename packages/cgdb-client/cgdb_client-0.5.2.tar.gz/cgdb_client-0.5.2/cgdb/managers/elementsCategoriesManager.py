from cgdb.resources.elementsCategory import ElementsCategory
from cgdb.utils.ManagerMix import ManagerMix


class ElementsCategoriesManager(ManagerMix):
    def __init__(self, client):
        super().__init__(client)

    def elementsCategories(self):
        content = self.get("/element-categories")
        element_categories = []

        for element_category_raw in content:
            element_categories.append(ElementsCategory(**element_category_raw, client=self._client))

        return element_categories

    def elementsCategory(self, code):
        content = self.get("/element-categories/" + code)

        return ElementsCategory(**content, client=self._client)
