import unittest
from order_book import OrderBook
from io import StringIO
from unittest.mock import patch
import sys


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.order_book = OrderBook()

    def test_basic(self):
        with patch('sys.stdout', new=StringIO()):

            self.handle_inp('0,100000,1,1,1075')
            self.handle_inp('0,100001,0,1,1075')

            expected_output = '''
            2,1,1075
            3,100001
            3,100000
            '''
            expected_output = '\n'.join(expected_output.split()) + '\n'

            self.assertEqual(sys.stdout.getvalue(), expected_output)

    def test_invalid_cancel(self):
        with patch('sys.stderr', new=StringIO()):

            self.handle_inp('0,100000,1,1,1075')
            self.handle_inp('1,100001')

            self.assertEqual(sys.stderr.getvalue(), "\nBADMESSAGE - invalid order id\n")

    def test_given_example(self):
        with patch('sys.stdout', new=StringIO()) as testOutput, patch('sys.stderr', new=StringIO()) as testError:

            self.handle_inp('0,100000,1,1,1075')
            self.handle_inp('0,100001,0,9,1000')
            self.handle_inp('0,100002,0,30,975')
            self.handle_inp('0,100003,1,10,1050')
            self.handle_inp('0,100004,0,10,950')
            self.handle_inp('BADMESSAGE')
            self.handle_inp('0,100005,1,2,1025')
            self.handle_inp('0,100006,0,1,1000')
            self.handle_inp('1,100004')
            self.handle_inp('0,100007,1,5,1025')
            self.handle_inp('0,100008,0,3,1050')

            expected_output = '''
            2,2,1025
            4,100008,1
            3,100005
            2,1,1025
            3,100008
            4,100007,4
            '''
            expected_output = '\n'.join(expected_output.split()) + '\n'

            self.assertEqual(testOutput.getvalue(), expected_output)
            self.assertEqual(testError.getvalue(), "\nBADMESSAGE - invalid input\n")

    def test_large_sweep(self):
        with patch('sys.stdout', new=StringIO()) as testOutput, patch('sys.stderr', new=StringIO()) as testError:

            self.handle_inp('0,100000,1,1,1075')
            self.handle_inp('0,100001,0,9,1000')
            self.handle_inp('0,100002,0,30,975')
            self.handle_inp('0,100003,1,10,1050')
            self.handle_inp('0,100004,0,10,950')
            self.handle_inp('BADMESSAGE')
            self.handle_inp('0,100005,1,2,1025')
            self.handle_inp('0,100006,0,1,1000')
            self.handle_inp('1,100004')
            self.handle_inp('1,2,3,4,5') # Invalid message
            self.handle_inp('0,100007,1,5,1025')
            self.handle_inp('0,100008,0,100,1050')
            self.handle_inp('0,100009,1,100,900')

            expected_output = '''
            2,2,1025
            4,100008,98
            3,100005
            2,5,1025
            4,100008,93
            3,100007
            2,10,1050
            4,100008,83
            3,100003
            2,83,1050
            4,100009,17
            3,100008
            2,9,1000
            4,100009,8
            3,100001
            2,1,1000
            4,100009,7
            3,100006
            2,7,975
            3,100009
            4,100002,23
            '''
            expected_output = '\n'.join(expected_output.split()) + '\n'

            self.assertEqual(testOutput.getvalue(), expected_output)
            self.assertEqual(testError.getvalue(), """\nBADMESSAGE - invalid input\n\nBADMESSAGE - invalid input\n""")

    def handle_inp(self, str):
        self.order_book.handle_message(str)


if __name__ == '__main__':
    unittest.main()
