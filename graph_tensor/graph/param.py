class Param:
    def __init__(self):
        self.param = {}

    def __get__(self, obj, objtype):
        return self.param[obj]

    def __set__(self, obj, value):
        self.param[obj] = value
