# Создать декоратор с аргументами. Который будет вызывать функцию, определенное кол-во раз,
# будет выводить кол-во времени затраченного на выполнение данной функции и её название.

import time


def decorator(num_of_repeats=1):

    def inner_decorator(some_function):

        def wrapper(*args, **kwargs):

            res = []
            start_time = time.time()

            for i in range(num_of_repeats):

                result = some_function(*args, **kwargs)
                res.append(result)

            end_time = time.time()
            diff_time = end_time - start_time
            res.append(diff_time)

            return res

        return wrapper

    return inner_decorator


@decorator(100000)
def other_function(args):
    return other_function.__name__


print(other_function(1))

