class Writer(object):

    def __init__(self, data):
        self.data = data
        self.__should_write = False

class PostgresWriter(Writer):

    def __init__(self):
        super().__init__()


writer = Writer("this")
print(writer.data)