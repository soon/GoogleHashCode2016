__author__ = 'Andrew Kuchev (kuchevad@gmail.com)'


class Warehouse:
    def __init__(self, id, location, products):
        self.id = id
        self.location = location
        self.products = products


class Order:
    def __init__(self, id, target, product_types):
        self.id = id
        self.target = target
        self.product_types = product_types


class Command:
    def __init__(self, drone_id):
        self.drone_id = drone_id

    def __str__(self):
        raise NotImplementedError


class LoadCommand(Command):
    def __init__(self, drone_id, warehouse_id, product_type_id, products_count):
        super().__init__(drone_id)
        self.warehouse_id = warehouse_id
        self.product_type_id = product_type_id
        self.products_count = products_count

    def __str__(self):
        return '{} L {} {} {}'.format(self.drone_id, self.warehouse_id, self.product_type_id, self.products_count)


class UnloadCommand(Command):
    def __init__(self, drone_id, warehouse_id, product_type_id, products_count):
        super().__init__(drone_id)
        self.warehouse_id = warehouse_id
        self.product_type_id = product_type_id
        self.products_count = products_count

    def __str__(self):
        return '{} U {} {} {}'.format(self.drone_id, self.warehouse_id, self.product_type_id, self.products_count)


class DeliverCommand(Command):
    def __init__(self, drone_id, order_id, product_type_id, products_count):
        super().__init__(drone_id)
        self.order_id = order_id
        self.product_type_id = product_type_id
        self.products_count = products_count

    def __str__(self):
        return '{} D {} {} {}'.format(self.drone_id, self.order_id, self.product_type_id, self.products_count)


class WaitCommand(Command):
    def __init__(self, drone_id, turns_count):
        super().__init__(drone_id)
        self.turns_count = turns_count

    def __str__(self):
        return '{} W {}'.format(self.drone_id, self.turns_count)
