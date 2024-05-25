import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import List, Dict, Tuple
from chinese_remainder_theorem import chinese_reminder
from prime_factors import prime_factors
from collections import Counter
from tqdm.auto import tqdm
import math

# https://www.youtube.com/watch?v=007MVsELvQw
# b ** x = a mod p => x = logb(a)
def discrete_log_problem(b, a, p, upper_bound = 0):

    if upper_bound == 0:
        k = math.ceil(math.sqrt(p))
    else:
        k = math.ceil(math.sqrt(upper_bound))

    # Iterating over
    # b, b**2, b**3, b**4 ...
    normal_powers = []
    normal_powers_set = set()
    
    # Saving 
    # a*b**(-k), a*b**(-2*k), ...
    k_powers = []
    k_powers_set = set()

    # When a match is found, it means that
    # b ** n = a * b ** (-mk)
    # b**n * b**(mk) = a
    # b**(n + mk) = a
    # so return n + mk
    
    curr_normal_power = 1
    for i in tqdm(range(0, k)):

        if curr_normal_power == a:
            return i

        normal_powers.append(curr_normal_power)
        normal_powers_set.add(curr_normal_power)

        curr_normal_power = (curr_normal_power * b) % p



    b_powered_minus_1 = pow(b, p - 2, p)
    print("b**-1 = " + str(b_powered_minus_1))
    
    b_powered_minus_k = pow(b_powered_minus_1, k, p)
    print("b**-k = " + str(b_powered_minus_k))

    # First calculate ak_powers
    curr_bk_power = 1
    for i in tqdm(range(0, k)):

        curr_k_power = (a * curr_bk_power) % p

        if curr_k_power in normal_powers_set:
            j = normal_powers.index(curr_k_power)
            
            # a * b ** (-k*i) = b ** j => a = b ** (k*i + j)
            return k*i + j
            
        k_powers.append(curr_k_power)
        k_powers_set.add(curr_k_power)

        curr_bk_power = (curr_bk_power * b_powered_minus_k) % p
        
    
    raise Exception("Could not find bsgs")


if __name__ == "__main__":
    x = discrete_log_problem(3, 19, 59)
    print(x)
    print(pow(3, x, 59))

    
