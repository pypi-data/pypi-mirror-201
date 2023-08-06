class Parameter:
    def __init__(self, id:int = None, name:str = None, description:str=None, type:str=None, created:int=None, last_updated:int=None, client=None):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.created = created
        self.last_updated = last_updated

        self.client = client