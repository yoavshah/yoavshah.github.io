import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import List, Dict, Tuple
from chinese_remainder_theorem import chinese_reminder, chinese_reminder_faster
from prime_factors import prime_factors
from collections import Counter
from tqdm.auto import tqdm
import math

import baby_step_giant_step as bsgs
import pohlig_hellman as ph



# b ** x = a mod p => x = logb(a)
# A discrete log algorithm that uses pohlig-hellman and then bgsg, then uses chinese reminder
# to find the discrete log
def discrete_log(b, a, p):
    phi_p = p - 1
    
    factors = prime_factors(phi_p)
    factors_cnt = Counter(factors)
    
    prime_factors_phi_mult = 1
    for curr_factor in factors:
        prime_factors_phi_mult *= curr_factor


    reminders = [] 
    for factor in factors_cnt:
        power = factors_cnt[factor]
        factor_powered = pow(factor, power)

        other_factors_mults = prime_factors_phi_mult // factor_powered
        
        # Let x = a0 + factor_phi[i]
        # So b ** x mod p = b ** (a0 + factor_phi[i]) mod p
        # => b**a0 * b**factor_phi[i] mod p = a mod p

        # b**(a0 * other_factors_mults) * b**(factor_phi[i]*other_factors_mults) mod p = a ** other_factors_mults mod p

        # = b ** (a0 * other_factors_mults) mod p = a ** other_factors_mults

        # In other words we need to find a0 for the equation below (we have all other parameters)
        # a0 is between 0 to factor_powered 
        # => (b ** other_factors_mults) ** a0 mod p = a ** other_factors_mults

        b_powered = pow(b, other_factors_mults, p)
        a_powered = pow(a, other_factors_mults, p)

        print(f"Find x such that {b_powered}**x mod {p} = {a_powered}")
        a0 = bsgs.discrete_log_problem(b_powered, a_powered, p, factor_powered)
        print(f"Found x = {a0}")
        print("-" * 20)

        is_prime = factors_cnt[factor] == 1
        reminders.append((a0, factor_powered, is_prime))


    print("Finding the solution using the chinese reminder " + str(reminders))
    return chinese_reminder_faster(reminders)
        




if __name__ == "__main__":
    x = discrete_log(3, 23, 31)
    print(x)
    print(f"{pow(3, x, 31)} = 23")
