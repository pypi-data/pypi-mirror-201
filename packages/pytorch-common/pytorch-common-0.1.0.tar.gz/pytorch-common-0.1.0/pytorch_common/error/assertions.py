from pytorch_common.error import Checker


class Assertions:
    @staticmethod
    def positive_int(error_code, value, name):
        Checker(error_code, value, name).is_not_none().is_int().is_positive().check()

    @staticmethod
    def positive_float(error_code, value, name):
        Checker(error_code, value, name).is_not_none().is_float().is_positive().check()

    @staticmethod
    def is_class(error_code, value, name, _class):
        Checker(error_code, value, name).is_not_none().is_a(_class).check()

    @staticmethod
    def is_tensor(error_code, value, name):
        Checker(error_code, value, name).is_not_none().is_tensor().check()

    @staticmethod
    def has_shape(error_code, value, shape, name):
        Checker(error_code, value, name).is_not_none().is_tensor().has_shape(shape).check()
