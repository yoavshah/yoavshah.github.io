import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import List, Dict, Tuple
from chinese_remainder_theorem import chinese_reminder
from prime_factors import prime_factors
from collections import Counter
from tqdm import tqdm


# https://www.youtube.com/watch?v=SmzUe_-e7oA 
# b ** x = a mod p => x = logb(a)
def discrete_log_problem(b, a, p):

    phi_p = p - 1

    print("Finding factors of phi(p)")
    prime_factors_phi = prime_factors(phi_p)

    print("Found: " + str(prime_factors_phi))
    prime_cnt = Counter(prime_factors_phi)
    
    prime_factors_phi_mult = 1
    for curr_factor in prime_factors_phi:
        prime_factors_phi_mult *= curr_factor

        
    reminders = []
    for curr_factor in prime_cnt:

        factor_powered = curr_factor ** prime_cnt[curr_factor]

        other_factors_mults = prime_factors_phi_mult // factor_powered
        
        # Let x = a0 + factor_phi[i]

        # So b ** x mod p = b ** (a0 + factor_phi[i]) mod p

        # => b**a0 * b**factor_phi[i] mod p = a mod p

        # b**(a0 * other_factors_mults) * b**(factor_phi[i]*other_factors_mults) mod p = a mod p

        # = b ** (a0 * other_factors_mults) mod p = a ** other_factors_mults

        # => (b ** other_factors_mults) ** a0 mod p = a ** other_factors_mults

        b_powered = pow(b, other_factors_mults, p)
        a_powered = pow(a, other_factors_mults, p)

        print("a = " + str(a))
        print("b = " + str(b))
        print(str(b) + " ** " + str(other_factors_mults) + " ** a0 = " + str(a) + " ** " + str(other_factors_mults) + " mod " + str(p))
        print(str(b_powered) + " ** a0 = " + str(a_powered) + " mod " + str(p))
        print("Brute forcing until number " + str(factor_powered))
        print("-"*20)

        curr_powered = 1
        for test_n in tqdm(range(factor_powered)):
            if curr_powered == a_powered:
                reminders.append((test_n, factor_powered))
                break

            curr_powered = (curr_powered * b_powered) % p

        print("-"*20)

    print("Finding the solution using the chinese reminder " + str(reminders))
    return chinese_reminder(reminders)

        

if __name__ == "__main__":
    
    # 3 ** x == 22 mod 31
    print(discrete_log_problem(7, 26, 41))
