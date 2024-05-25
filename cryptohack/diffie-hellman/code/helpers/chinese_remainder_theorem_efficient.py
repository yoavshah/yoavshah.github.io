from typing import List, Dict, Tuple

# https://www.youtube.com/watch?v=oKMYNKbFHBE
# Written by me

def egcd(a, b):
    """Extended Euclidean Algorithm
    returns (g, x, y) such that a*x + b*y = g = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m
    
def chinese_reminder(reminders : List[Tuple[int, int]]):
    summed_value = 0
    mods_mults = 1
    
    for i, tup in enumerate(reminders):
        reminder = tup[0]
        mod = tup[1]
        mods_mults *= mod
        

        # Create number that is = 0 mod (other reminders)
        mul = 1
        for j, curr_tup in enumerate(reminders):
            if j != i:
                mul *= curr_tup[1]

        mul_inv = modinv(mul, mod)
        curr_mul = mul_inv * mul
        
        summed_value += (curr_mul * reminder)


    return summed_value % mods_mults




        
if __name__ == "__main__":
    arr = [(3, 8, False), (1, 3, False), (126, 293, False), (579, 5417, False),  (351823381944, 420233272499, True)]
    n = chinese_reminder(arr)
    print(n)

    for r, m, p in arr:
        if n % m != r:
            print(f"bad {n} % {m} = {n % m} != {r}")
            break
    else:
        print("good")
    
