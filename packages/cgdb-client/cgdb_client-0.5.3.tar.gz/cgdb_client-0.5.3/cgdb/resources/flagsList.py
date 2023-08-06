class FlagList:
    def __init__(self, id:int, name:str=None, descripton:str=None, created:int=None, last_update:int=None, flags=None, client=None):
        self.id = id
        self.name = name
        self.descripton = descripton
        # self.created = created
        # self.last_update = last_update
        self.flags = []

        self.client = client
