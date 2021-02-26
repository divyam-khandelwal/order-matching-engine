import sys
from order_book import OrderBook

order_book = OrderBook()

for line in sys.stdin:
    order_book.handle_message(line)
