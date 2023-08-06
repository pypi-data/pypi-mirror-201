import torch

from pytorch_common.error import CommonException


class Expression:
    def __init__(self, expression_fn, message_fn):
        self.__expression_fn = expression_fn
        self.message_fn = message_fn
        self.message = None

    def exec(self, value):
        result = self.__expression_fn(value)

        if not result:
            self.message = self.message_fn(value)

        return result


class Checker:
    def __init__(self, error_code, value, name='Value'):
        self.__expressions = []
        self.__error_code = error_code
        self.__value = value
        self.__name = name

    def is_not_none(self):
        self.__expressions.append(Expression(lambda it: it is not None, lambda it: f'{self.__name} is None'))
        return self

    def is_int(self):
        self.__expressions.append(Expression(lambda it: isinstance(it, int), lambda it: f'{self.__name} is not int'))
        return self

    def is_float(self):
        self.__expressions.append(
            Expression(lambda it: isinstance(it, float), lambda it: f'{self.__name} is not float'))
        return self

    def is_positive(self):
        self.__expressions.append(Expression(lambda it: it >= 0, lambda it: f'{self.__name} is not a positive number'))
        return self

    def is_a(self, _class):
        self.__expressions.append(
            Expression(lambda it: isinstance(it, _class), lambda it: f'{self.__name} is not a {_class.__name__}'))
        return self

    def is_tensor(self):
        self.is_a(torch.Tensor)
        return self

    def has_shape(self, shape):
        self.__expressions.append(Expression(
            lambda it: len(it.size()) == len(shape),
            lambda it: f'{self.__name} has wrong dims count!. Expected: {shape}, Current: {it.size()}'
        ))
        self.__expressions.append(Expression(
            lambda it: self.__assert_shape(it, shape),
            lambda it: f'{self.__name} has invalid shape! Expected: {shape}, Current: {it.size()}'
        ))
        return self

    def check(self):
        errors = self.__errors()
        if errors:
            raise CommonException(self.__error_code, errors)

    def __errors(self):
        return [exp.message for exp in self.__expressions if not exp.exec(self.__value)]

    def __assert_shape(self, tensor, expected_shape):
        return all([td == ed for td, ed in zip(tensor.size(), expected_shape) if ed != -1])
