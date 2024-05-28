import math
from tqdm import tqdm

def prime_factors(n):
    
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n = n // 2


    i = 3
    n_sqrt = math.isqrt(n)
    while i <= n_sqrt and n != 1:
        if n % i != 0:
            i += 2
            
        else:
            n //= i
            factors.append(i)

        
            
    if n > 1:
        factors.append(n)
        
    return factors



if __name__ == "__main__":
    print(prime_factors(5000))
