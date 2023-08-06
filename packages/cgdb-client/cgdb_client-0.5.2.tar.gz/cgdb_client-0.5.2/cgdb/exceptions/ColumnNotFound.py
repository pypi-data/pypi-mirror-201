class ColumnNotFoundException(Exception):
    def __init__(self, column_name, message="Column in data frame not fond"):
        self.column_name = column_name
        self.message = message
        super().__init__(self.message)