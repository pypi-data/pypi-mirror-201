from enum import Enum

class OverwriteStrategy(Enum):
    OVERWRITE = 'OVERWRITE'
    CREATE_NEW = 'CREATE_NEW'
    IGNORE_NEW = 'IGNORE_NEW'
