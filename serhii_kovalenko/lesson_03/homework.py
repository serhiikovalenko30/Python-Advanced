# Создать класс структуры данных Стек, Очередь.
class List:
    _list = None

    def __new__(cls, *args, **kwargs):
        if not cls._list:
            cls._list = super().__new__(cls)
            return cls._list
        raise Exception('List already exists')

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        return self._items.pop(0)

    def size(self):
        return len(self._items)

    def is_empty(self):
        return True if not self.size() else False


class Stack(List):
    def dequeue(self):
        return self._items.pop()


class Queue(List):
    pass


# Создать класс комплексного числа и реализовать для него арифметические операции.

class Complex:
    __slots__ = ('_real', '_imag')

    def __init__(self, _real=0, _imag=0):
        self._real = _real
        self._imag = _imag

    def __str__(self):
        if self._real != 0 and self._imag != 0:
            if self._imag == 1:
                return str(self._real) + '+i'
            if self._imag == -1:
                return str(self._real) + '-i'
            return str(self._real) + ('+' if self._imag > 0 else '') + str(self._imag) + 'i'
        elif self._real != 0:
            return str(self._real)
        elif self._imag != 0:
            if self._imag == 1:
                return 'i'
            if self._imag == -1:
                return '-i'
            return str(self._imag) + 'i'
        else:
            return '0'

    def __add__(self, other):
        real, imag = self._real + other._real, self._imag + other._imag
        return Complex(real, imag)

    def __sub__(self, other):
        real, imag = self._real - other._real, self._imag - other._imag
        return Complex(real, imag)

    def __mul__(self, other):
        real = self._real * other._real - self._imag * other._imag
        imag = self._real * other._imag + self._imag * other._real
        return Complex(real, imag)

    def __truediv__(self, other):
        sum_of_squares = (other._real ** 2 + other._imag ** 2)
        real = (self._real * other._real + self._imag * other._imag) / sum_of_squares
        imag = (other._real * self._imag - self._real * other._imag) / sum_of_squares
        return Complex(real, imag)
