class Proxy(object):
    def __init__(self, local, name=None):
        object.__setattr__(self, '_Proxy__local', local)
        object.__setattr__(self, '__name__', name)

    def _get_current_object(self):
        if callable(self.__local):
            return self.__local()
        try:
            return getattr(self.__local, self.__name__)
        except AttributeError:
            raise RuntimeError('no object bound to %s' % self.__name__)

    def __getattr__(self, name):
        return getattr(self._get_current_object(), name)

    def __setattr__(self, name, value):
        setattr(self._get_current_object(), name, value)

    def __delattr__(self, name):
        delattr(self._get_current_object(), name)

    def __str__(self):
        return str(self._get_current_object())


class Car(object):
    def __init__(self, brand, models=None):
        self.brand = brand
        self.models = [] if models is None else models


class Stack(object):
    def __init__(self):
        self.items = []

    def push(self, obj):
        self.items.append(obj)

    def pop(self):
        return self.items.pop()

    @property
    def top(self):
        return self.items[len(self.items)-1]


car = Car('BMW', ['X1'])
models = Proxy(car, 'models')
print(models)
car.models = ['X5']
print(models)

cars = Stack()
current_car = Proxy(lambda: cars.top)
car_foo = Car('BMW')
car_foo.models.append('X1')
cars.push(car_foo)
car_bar = Car('TESLA')
car_bar.models.append('S')
cars.push(car_bar)
print(current_car.brand, current_car.models)
cars.pop()
print(current_car.brand, current_car.models)
