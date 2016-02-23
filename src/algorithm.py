#!/usr/bin/env python3
import random

import itertools
from collections import Counter

import math
from pprint import pprint

from models import Warehouse, Order, Drone, LoadCommand, DeliverCommand


class MagicCommandPredictor:
    def __init__(self, drones_count, max_turns_count, max_payload, product_type_weights, warehouses, orders):
        self.drones = [Drone(i, warehouses[0].location, 0) for i in range(drones_count)]
        self.orders = orders
        self.warehouses = warehouses
        self.max_turns_count = max_turns_count
        self.max_payload = max_payload
        self.product_type_weights = {t: w for t, w in enumerate(product_type_weights)}

    def predict_commands_for_orders(self, orders):
        return itertools.chain.from_iterable(self.predict_commands_for_order(o) for o in orders)

    def predict_commands_for_order(self, order):
        drones = self.drones[:]
        required_products = Counter(order.products)
        nearest_warehouses = sorted([w.clone() for w in self.warehouses], key=order.distance_to)
        loaded_drones = []

        for w in nearest_warehouses:
            products_to_be_taken = required_products & w.products
            while products_to_be_taken:
                nearest_drone = self.find_nearest_drone(w, drones)
                products_in_drone = self.load_drone(products_to_be_taken)
                released_drone = nearest_drone.load_at_warehouse_and_deliver_to_order(w, products_in_drone, order)
                products_to_be_taken -= products_in_drone
                w.products -= products_in_drone
                required_products -= products_in_drone
                loaded_drones.append((nearest_drone, released_drone, order, w, products_in_drone))
                drones.remove(nearest_drone)
                drones.append(released_drone)

        if required_products:
            return []

        if not loaded_drones:
            return []

        max_release = max(d[1].releases_at for d in loaded_drones)
        if max_release > self.max_turns_count:
            return []
        else:
            self.drones = drones
            self.warehouses = nearest_warehouses
            return self.generate_commands_for_drones(loaded_drones)

    def load_drone(self, total_number_of_products):
        products_to_be_taken = Counter()
        for t, c in total_number_of_products.items():
            weight = self.calculate_total_weight(products_to_be_taken)
            if weight >= self.max_payload:
                break
            c1 = min(c, math.floor((self.max_payload - weight) / self.product_type_weights[t]))
            if c1 > 0:
                products_to_be_taken[t] = c1

        return products_to_be_taken

    def calculate_total_weight(self, products):
        return sum(c * self.product_type_weights[t] for t, c in products.items())

    def find_nearest_drone(self, map_object, drones):
        min_release = min(d.releases_at for d in drones)
        return min(drones, key=lambda d: d.time_to(map_object) + d.releases_at - min_release)

    def generate_commands_for_drones(self, loaded_drones):
        return list(itertools.chain.from_iterable(
                self.generate_command_for_drone(d1, o, w, p) for d1, d2, o, w, p in loaded_drones))

    def generate_command_for_drone(self, drone, order, warehouse, products):
        load_commands = [LoadCommand(drone.id, warehouse.id, t, c) for t, c in products.items()]
        deliver_commands = [DeliverCommand(drone.id, order.id, t, c) for t, c in products.items()]
        return load_commands + deliver_commands


def read_warehouse(id):
    location = tuple(int(x) for x in input().split())
    products = [int(x) for x in input().split()]

    return Warehouse(id, location, products)


def read_order(id):
    target = tuple(int(x) for x in input().split())
    product_types_n = int(input())
    product_types = [int(x) for x in input().split()]

    return Order(id, target, product_types)


def randomize_orders(orders):
    shuffled = orders[:]
    random.shuffle(shuffled)
    return shuffled


def run_test():
    rows, cols, drones_n, turns_n, max_payload = 100, 100, 3, 50, 500
    product_types_weights = [100, 5, 450]
    warehouses = [
        Warehouse(0, [0, 0], [5, 1, 0]),
        Warehouse(1, [5, 5], [0, 10, 2]),
    ]
    orders = [
        Order(0, (1, 1), [2, 0]),
        Order(1, (3, 3), [0, 0, 0]),
        Order(2, (5, 6), [2])
    ]

    predictor = MagicCommandPredictor(drones_n, turns_n, max_payload, product_types_weights, warehouses, orders)
    randomized_orders = randomize_orders(orders)
    commands = list(predictor.predict_commands_for_orders(randomized_orders))

    commands_str = [str(c) for c in commands]
    print(len(commands_str))
    print('\n'.join(commands_str))


def main():
    rows, cols, drones_n, turns_n, max_payload = [int(x) for x in input().split()]
    product_types_n = int(input())
    product_types_weights = [int(x) for x in input().split()]

    warehouses_n = int(input())
    warehouses = [read_warehouse(i) for i in range(warehouses_n)]

    order_n = int(input())
    orders = [read_order(i) for i in range(order_n)]

    predictor = MagicCommandPredictor(drones_n, turns_n, max_payload, product_types_weights, warehouses, orders)
    commands = list(predictor.predict_commands_for_orders(randomize_orders(orders)))

    pprint(commands)
    commands_str = [str(c) for c in commands]
    print(len(commands_str))
    print('\n'.join(commands_str))


if __name__ == '__main__':
    main()
