# task 1
class Car:
    def __init__(self, brand, engine):
        self._brand = brand
        self._engine = engine
        self._fuel = 0

    def get_brand(self):
        return self._brand

    def set_brand(self, value):
        self._brand = value

    def get_engine(self):
        return self._engine

    def set_engine(self, value):
        self._engine = value

    def _set_fuel(self, value):
        self._fuel += value

    def _get_fuel(self, value):
        return self._fuel

    def move(self):
        print(f'I move')


class Truck(Car):
    def __init__(self, brand, engine):
        super().__init__(brand, engine)
        self._shipping_weight = 100

    def move(self):
        print(f'I am truck, and i move 10 km per hour')

    def _get_shipping_weight(self):
        return self._shipping_weight

    def _set_shipping_weight(self, value):
        self._shipping_weight = value


class Passenger(Car):
    def __init__(self, brand, engine):
        super().__init__(brand, engine)
        self._number_of_passengers = 4

    def move(self):
        print(f'I am passenger car, and i move 10 km per hour')

    def _get_number_of_passengers(self):
        return self._number_of_passengers

    def _set_number_of_passengers(self, value):
        self._number_of_passengers = value


print(Car('bmw', 'v8').__dict__)
print(Truck('caterpillar', 'v20').__dict__)
print(Passenger('opel', 'v3').__dict__)


# task 2
class Store:
    QUANTITY_OF_GOODS_SOLD = 0

    def __init__(self, store_name, quantity_of_goods_sold):
        self._store_name = store_name
        self._quantity_of_goods_sold = quantity_of_goods_sold
        self._set_total_quantity_of_goods_sold(quantity_of_goods_sold)

    def _get_quantity_of_goods_sold(self):
        return self._quantity_of_goods_sold

    def _set_quantity_of_goods_sold(self, quantity):
        self._quantity_of_goods_sold += quantity
        self._set_total_quantity_of_goods_sold(quantity)

    def _get_total_quantity_of_goods_sold(self):
        return Store.QUANTITY_OF_GOODS_SOLD

    def _set_total_quantity_of_goods_sold(self, quantity):
        Store.QUANTITY_OF_GOODS_SOLD += quantity


store1 = Store('booking', 0)
store2 = Store('rozetka', 0)

store1._set_quantity_of_goods_sold(10)
store2._set_quantity_of_goods_sold(50)

print(store1._get_total_quantity_of_goods_sold())


# task 3
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_x(self, value):
        self.x = value

    def set_y(self, value):
        self.y = value

    def set_z(self, value):
        self.z = value

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def custom_add(self, other_point):
        new_x = self.get_x() + other_point.get_x()
        new_y = self.get_y() + other_point.get_y()
        new_z = self.get_z() + other_point.get_z()
        return Point(new_x, new_y, new_z)

    def custom_sub(self, other_point):
        new_x = self.get_x() - other_point.get_x()
        new_y = self.get_y() - other_point.get_y()
        new_z = self.get_z() - other_point.get_z()
        return Point(new_x, new_y, new_z)

    def custom_mul(self, other_point):
        new_x = self.get_x() * other_point.get_x()
        new_y = self.get_y() * other_point.get_y()
        new_z = self.get_z() * other_point.get_z()
        return Point(new_x, new_y, new_z)

    def custom_div(self, other_point):
        new_x = self.get_x() / other_point.get_x()
        new_y = self.get_y() / other_point.get_y()
        new_z = self.get_z() / other_point.get_z()
        return Point(new_x, new_y, new_z)

    def custom_eq(self, other_point):
        if self.get_x() == other_point.get_x() and self.get_y() == other_point.get_y() \
                and self.get_z() == other_point.get_z():
            return True

    def custom_ne(self, other_point):
        if self.get_x() != other_point.get_x() or self.get_y() != other_point.get_y() \
                or self.get_z() != other_point.get_z():
            return True


point = Point(1, 2, 3)
point2 = Point(1, 2, 3)
print(point.custom_mul(point2).__dict__)
print(point.custom_eq(point2))
print(point.custom_ne(point2))
