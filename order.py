class Order(object):
    def __init__(self, args, event_num):

        if int(args[0]) == 0:
            self.event_num = event_num
            self.message_type = int(args[0])
            self.order_id = int(args[1])
            self.side = int(args[2])
            self.quantity = int(args[3])
            self.price = float(args[4])

        elif int(args[0]) == 1:
            self.event_num = event_num
            self.message_type = int(args[0])
            self.order_id = int(args[1])

    def __lt__(self, other):
        if self.message_type == 0:

            # BUY
            if self.side == 0:
                if self.price > other.price:
                    return True
                elif self.price == other.price:
                    return True if self.event_num < other.event_num else False
                else:
                    False

            # SELL
            elif self.side == 1:
                if self.price < other.price:
                    return True
                elif self.price == other.price:
                    return True if self.event_num < other.event_num else False
                else:
                    False

    def modify_quantity(self, new_quantity, event_num):
        self.event_num = event_num
        self.quantity = new_quantity
