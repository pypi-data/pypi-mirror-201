import logging


class LoggerBuilder:
    def __init__(self):
        self.__clean_previous_handlers = False
        self.__handlers = []
        self.__level = logging.INFO

    def level(self, level):
        self.__level = level
        return self

    def clean_prev_handlers(self):
        self.__clean_previous_handlers = True
        return self

    def handler(self, handler):
        self.__handlers.append(handler)
        return self

    def on_console(self, format='%(asctime)s - %(levelname)s - %(message)s'):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(format))
        return self.handler(handler)

    def build(self):
        logger = logging.getLogger()

        if self.__clean_previous_handlers:
            logger.handlers.clear()

        [logger.addHandler(h) for h in self.__handlers]

        logger.setLevel(self.__level)

        return logger
