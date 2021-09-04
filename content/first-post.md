title: Blog on Homework 1
date: 09/03/2021
author: Gaojia Xu


In this blog, my solutions of 3 small questions from [Euler Project](https://projecteuler.net/archives) will be explained. They are problem 6, 34 and 80.

Blog outline:

* [1.1 Sum square difference](#section1)
* [1.2 Digit factorials](#section2)
* [1.3 Square root digital expansion](#section3)


##1.1 Sum square difference<a name="section1"></a>
This is problem 6 from the [Euler Project](https://projecteuler.net/archives). Solved by 496,347 up to now.

Here is the question: Find the difference between the sum of the squares of the first 100 natural numbers and square of their sum.

This question is quite straightforward. 

1. The square of the sum of first 100 numbers can be computed directly. 
2. We can loop through the 100 numbers to calculate the square of each number then sum them up. 
3. The final step is finding difference of these two components by subtraction.

The function looks like this:

```python

def square_diff():
    """Return difference of the sum of squares of first 100 number and square of their sum."""
    lst = range(1, 101)    
    return sum(lst) ** 2 - sum(s ** 2 for s in lst)
  
```

##1.2 Digit factorials<a name="section2"></a>
This is problem 34 from the [Euler Project](https://projecteuler.net/archives). Solved by 95,112 up to now.

Here is the question: Find the sum of all numbers which are equal to the sum of the factorial of their digits.

The intuitive train of thought is to first check the sum of the factorial of the digits, then if this sum equals to the number, means it satisfies the criteria, we should add the number to the final sum.

1. As we know the there are only 9 kinds of factorial result of a digit, so I first create the factorial dictionary in order to simplify the further repeated factorial calculations.

2. To choose the upper bound of the loop range, we know if the number has more than 7 digits, then no matter how many digits it has, say n, then multiply n by 9! will less than the number itself. Thus we can choose the upper bound as factorial of 9 multiplied by 7 to save energy. Also from the problem, we follow the instructions to exclude 1 and 2 so the lower bound is 3.

3. Then the main idea to calculate sum of the factorial of the digits is converting the number to string for the inner loop of digits' factorial. Make digits in the number to a list and find corresponding factorial from the factorial list for further summation.

4. Finally, after checking the equalization of sum of digits factorial and the number, we can add satisfied numbers to the total sum.


The function looks like this:

```
import math

def dig_factorial():
    """Return sum of all numbers which are equal to the sum of the factorial of their digits."""    

    # create factorial dictionary for simplicity
    fact_list = [math.factorial(x) for x in range(0,10)]
    tot_sum = 0
    
    for i in range(3, math.factorial(9) * 7):
        if sum([fact_list[int(j)] for j in str(i)]) == i:
            tot_sum += i      
    
    return tot_sum

```

##1.3 Square root digital expansion<a name="section3"></a>
This is problem 80 from the [Euler Project](https://projecteuler.net/archives). Solved by 19,755 up to now.

Here is the Question: For the first one hundred natural numbers, find the total of the digital sums of the first one hundred decimal digits for all the irrational square roots.

A thing I noticed is that if we find square root of a number directly, it will only return several digits which is not enough for this question. Thus, we can leverage the package `decimal` to extract decimal with specified precision.

1. The logic of this question is firstly, check if the number has irrational square root, if the residual of the square root divided by 1 is not 0, this means the number is irrational.

2. Then we process the number to find summation of its digit. But before that we should replace the dot in square root of the number to nothing in order to do summation easier. Checking with the question in Euler, it says for square root of number 2, digital sum of its first one hundred decimal digits is 475, which is the sum of digits start from the very beginning (including the integer part), so we stick with this rule.

3. For each irrational number, we design a inner loop of digits to calculate sum. The idea is similar to the second question, which is making digits first into string and then convert back. Finally, we add all digital sums of  first 100 digits of irrational square roots in first 100 number.


The function looks like this:

```
from decimal import *

def root_expan():
    """Return total of the digital sums of the first 100 decimal digits for all the irrational square roots"""
    
    getcontext().prec = 102   
    tot = 0
    for i in range(101):
        
        # indicates the square root of the number is irrational
        if math.sqrt(i) % 1 != 0 : 
            dec_string = str(Decimal(i).sqrt()).replace('.', '')[:100]             
            sum_dec = 0
            for j in dec_string:
                sum_dec += int(j)
            tot += sum_dec
            
    return tot


```

