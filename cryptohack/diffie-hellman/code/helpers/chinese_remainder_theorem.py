from typing import List, Dict, Tuple
from tqdm import tqdm

# https://www.youtube.com/watch?v=oKMYNKbFHBE
# Written by me

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

  
            
        # Iterate over that number until we find 
        mul_index = 1
        while True:
            curr_mul = mul * mul_index

            if curr_mul % mod == 1:
                break
                
            mul_index += 1

  
        summed_value += (curr_mul * reminder)


    return summed_value % mods_mults


def chinese_reminder_faster(reminders : List[Tuple[int, int, bool]]):
    summed_value = 0
    mods_mults = 1
    
    for i, tup in tqdm(enumerate(reminders)):
        reminder = tup[0]
        mod = tup[1]
        is_mod_prime = tup[2]
        mods_mults *= mod
        

        # Create number that is = 0 mod (other reminders)
        mul = 1
        for j, curr_tup in enumerate(reminders):
            if j != i:
                mul *= curr_tup[1]

  
            
        # Iterate over that number until we find
        mul_inv = 1
        if is_mod_prime:
            mul_inv = pow(mul, mod - 2, mod)
            curr_mul = mul * mul_inv
            
        else:
            while True:
                curr_mul = mul * mul_inv

                if curr_mul % mod == 1:
                    break
                    
                mul_inv += 1

  
        summed_value += (curr_mul * reminder)


    return summed_value % mods_mults


        
if __name__ == "__main__":
    arr = [(3, 8, False), (1, 3, False), (126, 293, False), (579, 5417, False),  (351823381944, 420233272499, True)]
    n = chinese_reminder_faster(arr)
    print(n)

    for r, m, p in arr:
        if n % m != r:
            print(f"bad {n} % {m} = {n % m} != {r}")
            break
    else:
        print("good")
    
