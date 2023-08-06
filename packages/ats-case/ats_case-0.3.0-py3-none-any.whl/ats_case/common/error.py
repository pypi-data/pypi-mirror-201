class APIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "APIError - API服务接口[{}], 连接失败.".format(repr(self.value))
