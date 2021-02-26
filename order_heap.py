import heapq


class OrderHeap(object):

    def __init__(self):
        self.orders = []

    def insert(self, order):
        heapq.heappush(self.orders, order)

    def remove(self, order_id):
        self.orders = [order for order in self.orders if order.order_id != order_id]
        heapq.heapify(self.orders)

    def pop(self):
        return heapq.heappop(self.orders)

    def best_price(self):
        return self.orders[0].price
