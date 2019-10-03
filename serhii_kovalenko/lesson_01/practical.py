# Создать список из N элементов (от 0 до n с шагом 1). В этом списке вывести все четные значения.

n = 100
var_list = [i for i in [i for i in range(0, n)] if i % 2 == 0]
print(*var_list)

# Создать словарь Страна:Столица. Создать список стран. Не все страны со списка должны сходиться с названиями
# стран со словаря. С помощою оператора in проверить на вхождение элемента страны в словарь, и если такой
# ключ действительно существует вывести столицу.

dict_var = {'Ukraina': 'Kiev',
            'Russia': 'Moscow',
            'Italy': 'Rome',
            'Germany': 'Berlin'}

list_country = ['Ukraina', 'Russia', 'Italy', 'Spain']

for key, value in dict_var.items():
    if key in list_country:
        print(value)

# Напишите программу, которая выводит на экран числа от 1 до 100. При этом вместо чисел, кратных трем, программа
# должна выводить слово Fizz, а вместо чисел, кратных пяти — слово Buzz. Если число кратно пятнадцати,
# то программа должна выводить слово FizzBuzz.

for i in range(1, 101):
    if i % 15 == 0:
        print('FizzBuzz')
    elif i % 3 == 0:
        print('Fizz')
    elif i % 5 == 0:
        print('Buzz')
    else:
        print(i)

# Реализовать функцию bank, которая приннимает следующие аргументы: сумма депозита, кол-во лет, и процент.
# Результатом выполнения должна быть сумма по истечению депозита


def bank(deposit_sum, term, percent):
    days_a_year = 365
    sum_percent = (deposit_sum * (percent / 100) * (days_a_year * term)) / (days_a_year * 1)
    return deposit_sum + sum_percent


print(bank(100, 2, 20))
