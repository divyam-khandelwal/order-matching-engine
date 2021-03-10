# Order Matching Engine
Divyam Khandelwal - February 2021

# To Run

Code is tested on ```Python 3.6.1```.
```
# To RUN

cd ~/coding-exercise
python3 .
0,100000,1,1,1075
0,100001,0,9,1000
0,100002,0,30,975
0,100003,1,10,1050
0,100004,0,10,950
BADMESSAGE
0,100005,1,2,1025
0,100006,0,1,1000
1,100004
0,100007,1,5,1025
0,100008,0,3,1050
```
```
# OUTPUT

BADMESSAGE - invalid input
2,2,1025
4,100008,1
3,100005
2,1,1025
3,100008
4,100007,4
```

```
# To TEST

cd ~/coding-exercise
python3 -m unittest test
```


## Performance Characteristics
The matching engine uses two **heaps** (buy orders, sell orders) to keep track of the best bid/offers based on price and age.
Inserting orders has a time complexity of **O(log n)**, popping the "best" order has a  time complexity of **O(log n)**.

For an incoming aggressor that results in matches, the aggressor is first inserted into the heap [**O(log n)**], then the best matching orders are popped from the opposite heap [**O(log n)**] in the right priority. This popping of the best order continues until the aggressor quantity is satisfied or the prices don't overlap.

For a cancel, the time complexity is **O(n)**. The entire heap is traversed until the order is found, and then the heap is sorted again [**O(log n)**].

** *n* in the time complexity refers to the number of orders in the respective heap.




