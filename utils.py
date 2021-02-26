import sys

def args_valid(args):

    if len(args) == 5:
        # Check message type
        if int(args[0]) != 0:
            return False

        # Check order ID
        elif not positive_int(args[1]):
            return False

        # Check side
        elif not (int(args[2]) == 0  or int(args[2]) == 1):
            return False

        # Check quantity
        elif not positive_int(args[3]):
            return False

        # Check price
        elif not positive_float(args[4]):
            return False

        else:
            return True

    elif len(args) == 2:

        # Check message type
        if int(args[0]) != 1:
            return False

         # Check order ID
        elif not positive_int(args[1]):
            return False

        else:
            return True


def positive_int(inp_str):
    try:
        num = int(inp_str)
        return True if num > 0 else False
    except ValueError:
        return False


def positive_float(inp_str):
    try:
        float_val = float(inp_str)
        return True if float_val > 0 else False
    except ValueError:
        return False

def trade_event(quantity, price):
    if (price).is_integer():
        print(f"2,{quantity},{int(price)}", file=sys.stdout)
    else:
        print(f"2,{quantity},{price}", file=sys.stdout)

def complete_fill(order_id):
    print(f"3,{order_id}", file=sys.stdout)

def partial_fill(order_id, quantity):
    print(f"4,{order_id},{quantity}", file=sys.stdout)

