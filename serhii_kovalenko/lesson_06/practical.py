# Создать свою структуру данных Список, которая поддерживает индексацию.
# Методы pop, append, insert, remove, clear.
# Перегрузить операцию сложения для списков, которая возвращает новый расширенный объект.


class MyList:

    def __init__(self, *args):
        self._list = list(args)

    def __str__(self):
        return str(self._list)

    def __setitem__(self, key, value):
        self._list[key] = value

    def __getitem__(self, item):
        return self._list[item]

    def __delitem__(self, key):
        del self._list[key]

    def pop(self):
        del self[len(self._list) - 1]
        return self[len(self._list) - 1]

    def append(self, item):
        save_list = self._list
        self._list = [0] * (len(save_list) + 1)
        for i in range(len(save_list)):
            self._list[i] = save_list[i]
        self._list[-1] = item

    def insert(self, index, item):
        list_before_index = self._list[:index]
        list_after_index = self._list[index:]
        self._list = []
        for i in list_before_index:
            self.append(i)
        self.append(item)
        for i in list_after_index:
            self.append(i)

    def remove(self, item):
        for key, value in enumerate(self._list):
            if value == item:
                del self._list[key]
                break

    def claer(self):
        self._list = list()

    def __add__(self, other_list):
        result_list = []
        for i in self._list:
            result_list.append(i)
        for i in other_list:
            result_list.append(i)
        return MyList(*result_list)


# Создать свою структуру данных Словарь, которая поддерживает методы, get, items, keys, values.
# Так же перегрузить операцию сложения для словарей, которая возвращает новый расширенный объект.

class MyDict:

    def __init__(self, **kwargs):
        self._dict = dict(kwargs)

    def __str__(self):
        return str(self._dict)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, item):
        return self._dict[item]

    def __delitem__(self, key):
        del self._dict[key]

    def get(self, value):
        result = None
        for key in self.keys():
            if key == value:
                result = self._dict[key]
                break
        return result

    def items(self):
        keys_list, values_list = self.keys(), self.values()
        keys_values_list = []
        for key, value in enumerate(keys_list):
            keys_values_list.append((keys_list[key], values_list[key]))
        return keys_values_list

    def keys(self):
        return list(self._dict)

    def values(self):
        values_list = []
        for k in self.keys():
            values_list.append(self._dict[k])
        return values_list

    def __add__(self, other):
        return MyDict(**self._dict, **other)
