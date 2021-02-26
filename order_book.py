import sys
from order import Order
from order_heap import OrderHeap
from utils import args_valid, trade_event, partial_fill, complete_fill


class OrderBook(object):
    def __init__(self):
        self.buy_orders = OrderHeap()
        self.sell_orders = OrderHeap()
        self.order_ids = {}
        self.event_num = 0

    def handle_message(self, input_message):
        args = input_message.rstrip().split(",")

        if not args_valid(args):
            print("\nBADMESSAGE - invalid input", file=sys.stderr)

        else:
            self.event_num += 1
            order = Order(args, self.event_num)
            self.process_order(order)

    def process_order(self, order):

        # NEW order
        if order.message_type == 0 and order.order_id not in self.order_ids:
            self.buy_orders.insert(order) if order.side == 0 else self.sell_orders.insert(order)
            self.order_ids[order.order_id] = order.side
            self.run_matching_engine(order)

        # MODIFY order (Assumption: Existing orders can be modified)
        elif order.message_type == 0 and order.order_id in self.order_ids:
            previous_order_side = self.order_ids[order.order_id]
            self.order_ids[order.order_id] = order.side
            self.buy_orders.remove(order) if previous_order_side == 0 else self.sell_orders.remove(order)
            self.buy_orders.insert(order) if order.side == 0 else self.sell_orders.insert(order)
            self.run_matching_engine(order)

        # CANCEL order
        else:
            try:
                self.buy_orders.remove(order.order_id) if self.order_ids[order.order_id] == 0 else self.sell_orders.remove(order.order_id)
                del self.order_ids[order.order_id]
            except KeyError:
                print("\nBADMESSAGE - invalid order id", file=sys.stderr)

    def run_matching_engine(self, aggressor_order):

        # Incoming BUY
        if aggressor_order.side == 0:

            while aggressor_order.order_id in self.order_ids and self.prices_overlap():

                tob_order = self.sell_orders.pop()

                if tob_order.quantity < aggressor_order.quantity:
                    new_aggressor_quantity = aggressor_order.quantity - tob_order.quantity

                    trade_event(tob_order.quantity, tob_order.price)
                    partial_fill(aggressor_order.order_id, new_aggressor_quantity)
                    complete_fill(tob_order.order_id)

                    self.event_num += 1
                    aggressor_order.modify_quantity(new_aggressor_quantity, self.event_num)
                    self.buy_orders.remove(aggressor_order.order_id)
                    self.buy_orders.insert(aggressor_order)
                    del self.order_ids[tob_order.order_id]

                elif tob_order.quantity > aggressor_order.quantity:
                    new_tob_quantity = tob_order.quantity - aggressor_order.quantity

                    trade_event(aggressor_order.quantity, tob_order.price)
                    complete_fill(aggressor_order.order_id)
                    partial_fill(tob_order.order_id, new_tob_quantity)

                    self.event_num += 1
                    tob_order.modify_quantity(new_tob_quantity, self.event_num)
                    self.sell_orders.insert(tob_order)
                    self.buy_orders.remove(aggressor_order.order_id)
                    del self.order_ids[aggressor_order.order_id]

                else:

                    trade_event(aggressor_order.quantity, tob_order.price)
                    complete_fill(aggressor_order.order_id)
                    complete_fill(tob_order.order_id)

                    self.buy_orders.remove(aggressor_order.order_id)
                    del self.order_ids[aggressor_order.order_id]

        # Incoming SELL
        elif aggressor_order.side == 1:

            while aggressor_order.order_id in self.order_ids and self.prices_overlap():

                tob_order = self.buy_orders.pop()

                if tob_order.quantity < aggressor_order.quantity:
                    new_aggressor_quantity = aggressor_order.quantity - tob_order.quantity

                    trade_event(tob_order.quantity, tob_order.price)
                    partial_fill(aggressor_order.order_id, new_aggressor_quantity)
                    complete_fill(tob_order.order_id)

                    self.event_num += 1
                    aggressor_order.modify_quantity(new_aggressor_quantity, self.event_num)
                    self.sell_orders.remove(aggressor_order.order_id)
                    self.sell_orders.insert(aggressor_order)
                    del self.order_ids[tob_order.order_id]

                elif tob_order.quantity > aggressor_order.quantity:
                    new_tob_quantity = tob_order.quantity - aggressor_order.quantity

                    trade_event(aggressor_order.quantity, tob_order.price)
                    complete_fill(aggressor_order.order_id)
                    partial_fill(tob_order.order_id, new_tob_quantity)

                    self.event_num += 1
                    tob_order.modify_quantity(new_tob_quantity, self.event_num)
                    self.buy_orders.insert(tob_order)
                    self.sell_orders.remove(aggressor_order.order_id)
                    del self.order_ids[aggressor_order.order_id]

                else:

                    trade_event(aggressor_order.quantity, tob_order.price)
                    complete_fill(aggressor_order.order_id)
                    complete_fill(tob_order.order_id)

                    self.sell_orders.remove(aggressor_order.order_id)
                    del self.order_ids[aggressor_order.order_id]

    def prices_overlap(self):
        if self.buy_orders.orders and self.sell_orders.orders:
            return self.buy_orders.best_price() >= self.sell_orders.best_price()
        else:
            return False