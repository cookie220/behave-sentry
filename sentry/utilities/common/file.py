

class File:

    @staticmethod
    def read(filename):
        with open(filename, 'r') as reader:
            return reader.read()
