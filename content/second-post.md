title: Blog on Homework 2
date: 09/17/2021
author: Gaojia Xu

Number theory and a Google recruitment puzzle

In this blog, I will find the first 10-digit prime in the decimal expansion of 17π. We separate the question into 3 small functions and use them to create a main function.

Blog outline:

* [2.1 Generate expansion of expression.](#section1)
* [2.2 Check if a number is prime](#section2)
* [2.3 Generate sliding windows](#section3)
* [2.4 Unit test for former 3 functions](#section4)
* [2.5 Main function: find first n-digit prime in the decimal expansion of a number](#section5)
* [2.6 Unit test of main function](#section6)
* [2.7 Solve the problem](#section7)


##2.1 Generate expansion of expression<a name="section1"></a>

First we write a function to generate an arbitrary large expansion of a mathematical expression like π.

We can use directly from `sympy` package to expand an mathematical expression.

The function looks like this:

```python

from sympy import *

def expand(expression, expand_decimal):
    """Return the expression with decimal length specified"""
    
    if type(expand_decimal) not in [int, float]:
        raise TypeError("The specified digits length of expansion should be a float or an integer")
    
    return N(expression, expand_decimal)
  
```

##2.2 Check if a number is prime<a name="section2"></a>

Second, write a function to check if a number is prime.

The idea of this function : After considering some special case, such that number 2 is a prime, we can first sieve all even numbers because they are not prime, can be divided by 2. Then we can sieve multiples of odd numbers in a specific range, setting the upper bound as the square root of the number is economic way, and add 1 to be safer, and we skip the even numbers because we already sieve for 2. 

The function looks like this:

```python
def check_prime(n):
    """Check if the number is a prime"""
    if n == 2:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

```

##2.3 Generate sliding windows<a name="section3"></a>

Third, write a function to generate sliding windows of a specified width from a long iterable.

For each input number, create the sliding window from start position and with specified length, if there is dot included, we should split by dot and join all numbers from the int and decimal portion.


The function looks like this:

```
def sliding_window(num, start, length):
    """Return the string of the number starts from start position with specified length"""
    
    if type(start) != int or type(length) != int:
        raise TypeError("n_len and n_dec need to be integers")
    
    string = ''.join(str(num).split("."))[start : start + length]
    return string


```


##2.4 Unit test for 3 functions<a name="section4"></a>

We use unit test to check if 3 functions work.

```python

%%file functions.py

from sympy import *
import numpy as np


def expand(expression, expand_decimal):
    """Return the expression with decimal length specified"""
    
    if type(expand_decimal) not in [int, float]:
        raise TypeError("The specified digits length of expansion should be a float or an integer")
    
    return N(expression, expand_decimal)

def check_prime(n):
    """Check if the number is a prime"""
    if n == 2:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def sliding_window(num, start, length):
    """Return the string of the number starts from start position with specified length"""
    
    if type(start) != int or type(length) != int:
        raise TypeError("n_len and n_dec need to be integers")
    
    string = ''.join(str(num).split("."))[start : start + length]
    return string
```

```python

%%file test_functions.py

import math
import unittest
from functions import expand, check_prime, sliding_window


class TestHelpers(unittest.TestCase):
    def test_expand(self):
        self.assertEqual(str(expand(math.pi, 4)), format(math.pi, '.3f'))
        self.assertEqual(str(expand(math.e, 30)), format(math.e, '.29f'))
        self.assertEqual(str(expand(7.6*math.e, 8)), format(7.6*math.e, '.6f'))
    
    def test_expand_input(self):
        self.assertRaises(TypeError, expand, "5")
    
    def test_prime(self):
        self.assertTrue(check_prime(2))
        self.assertTrue(check_prime(5))
        self.assertTrue(check_prime(7427466391))
        self.assertFalse(check_prime(16))
        
    def test_gen(self):
        self.assertEqual(sliding_window(3.1415926589, 4, 3), '592')
        self.assertEqual(sliding_window(math.e, 6, 8), format(math.e, '.20f')[7:7+8])
    
if __name__ == '__main__':
    unittest.main()

```

```python

! python3 -m unittest test_functions.py

```

The test returns OK, which means three functions work well.

##2.5 Main function: find first n-digit prime in the decimal expansion of a number<a name="section5"></a>

1. For each expression, we first expand it to specified decimals, if it is not specified, we use default 1000.

2. We create sliding windows for the certain number of digit in the expanded expression. It should be a loop because we check from the beginning of the expanded expression and add 1 to the start position each time (shift the window to the right for 1 position each time).

3. Check if the number has length of the prime length we want, because if the number has 0 at the beginning, the length is shortened by 1, thus we set this as the one of the checking condition. And another checking condition is if the nubmer in sliding window is prime or not, and we only need the first prime.

```python

def prime_in_num(expression, prime_dig, expand_decimal = 1000):
    """Return the first prime of specified length in an expression"""
    
    expanded = expand(expression, expand_decimal)
    
    for i in range(expand_decimal):
        num_int = int(sliding_window(expanded, i, prime_dig))
        
        if (len(str(num_int)) == prime_dig) and (check_prime(num_int)):
            return num_int
        else: 
            i += 1
                
        if i > expand_decimal - prime_dig:
            return("There is no prime with specified length within the decimal expansion of the expression")
```

##2.6 Unit test of main function<a name="section6"></a>

What we know: The first 5 digits in the decimal expansion of π are 14159. The first 4-digit prime in the decimal expansion of π are 4159. The first 10-digit prime in the expansion e is 7427466391. We can use unit test to check if our main funciton returns the right answer.

```python

%%file main_function.py

from functions import expand, check_prime, sliding_window


def prime_in_num(expression, prime_dig, expand_decimal = 1000):
    """Return the first prime of specified length in an expression"""
    
    expanded = expand(expression, expand_decimal)
    
    for i in range(expand_decimal):
        num_int = int(sliding_window(expanded, i, prime_dig))
        
        if (len(str(num_int)) == prime_dig) and (check_prime(num_int)):
            return num_int
        else: 
            i += 1
                
        if i > expand_decimal - prime_dig:
            return("There is no prime with specified length within the decimal expansion of the expression")
```

```python

%%file test_main_function.py

from sympy import *
import math
import unittest
from functions import expand, check_prime, sliding_window
from main_function import prime_in_num

class TestHelpers(unittest.TestCase):
    def test_main(self):
        self.assertEqual(prime_in_num(E, 10), 7427466391)
        self.assertEqual(prime_in_num(math.pi, 5), 14159)
        self.assertEqual(prime_in_num(math.pi, 4), 4159)
    
if __name__ == '__main__':
    unittest.main()
```


```python

! python3 -m unittest test_main_function.py

```

The test returns OK, which means the main function works well.
    
   
##2.7 Solve the problem<a name="section7"></a>

Find 10-digit prime in decimal expansion of 17pi.

```python

prime_in_num(17*pi, 10)

```
The result returns 8649375157.

