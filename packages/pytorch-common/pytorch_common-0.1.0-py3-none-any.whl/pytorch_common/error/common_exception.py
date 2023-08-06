from abc import ABCMeta


class CommonException(Exception, metaclass=ABCMeta):
    def __init__(self, code, messages=['Exception']):
        message = ''
        for m in messages:
            message += f'{m}. '

        super().__init__(message)
        self.code = code
