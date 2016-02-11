import math
from collections import Counter


__author__ = 'Andrew Kuchev (kuchevad@gmail.com)'


class MapObject:
    def __init__(self, location):
        self.location = location

    def distance_to(self, map_object):
        return math.ceil(math.hypot(self.location[0] - map_object.location[0],
                                    self.location[1] - map_object.location[1]))

    def time_to(self, map_object):
        return self.distance_to(map_object) + 1


class Warehouse(MapObject):
    def __init__(self, id, location, products):
        super().__init__(location)
        self.id = id
        self.location = location
        if isinstance(products, Counter):
            self.products = Counter(products)
        else:
            self.products = Counter({i: p for i, p in enumerate(products)})

    def __repr__(self, *args, **kwargs):
        return 'Warehouse <{}, {}, {}>'.format(self.id, self.location, self.products)

    def clone(self):
        return Warehouse(self.id, self.location, self.products)


class Order(MapObject):
    def __init__(self, id, target, products):
        super().__init__(target)
        self.id = id
        self.target = target
        self.products = Counter(products)

    def __repr__(self, *args, **kwargs):
        return 'Order <{}, {}, {}>'.format(self.id, self.target, self.products)

    def clone(self):
        return Order(self.id, self.target, self.products.values())


class Drone(MapObject):
    def __init__(self, id, location, releases_at):
        super().__init__(location)
        self.id = id
        self.location = location
        self.releases_at = releases_at

    def __repr__(self, *args, **kwargs):
        return 'Drone <{}, {}, {}>'.format(self.id, self.location, self.releases_at)

    def load_at_warehouse_and_deliver_to_order(self, warehouse, products, order):
        return Drone(self.id, order.location,
                     self.releases_at + self.distance_to(warehouse) + warehouse.distance_to(order) + len(products) * 2)

    def clone(self):
        return Drone(self.id, self.location, self.releases_at)


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

    def __repr__(self, *args, **kwargs):
        return 'Load drone {} at WH {} with product type {} * {} items'.format(
                self.drone_id, self.warehouse_id, self.product_type_id, self.products_count)

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

    def __repr__(self, *args, **kwargs):
        return 'Deliver drone {} to order {} with product type {} * {} items'.format(
                self.drone_id, self.order_id, self.product_type_id, self.products_count)

    def __str__(self):
        return '{} D {} {} {}'.format(self.drone_id, self.order_id, self.product_type_id, self.products_count)


class WaitCommand(Command):
    def __init__(self, drone_id, turns_count):
        super().__init__(drone_id)
        self.turns_count = turns_count

    def __str__(self):
        return '{} W {}'.format(self.drone_id, self.turns_count)
