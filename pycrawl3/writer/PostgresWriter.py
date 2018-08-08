

class PostgresWriter(object):

    __data = set()
    __should_write = False

    def __init__(self, data):
        self.__data = data

    def add_data(self, data):
        self.__check_should_write()
        self.__data.add(data)

    def __check_should_write(self):
        if self.__should_write:
            self.write()
        elif len(self.__data) > 10:
            self.__should_write = True

    def __empty_data(self):
        self.__data = set()

    def write(self):
        self.__empty_data()
        self.__should_write = False
