p = 28151





t = 2
two_mults = []
while t not in two_mults:
    two_mults.append(t)
    t = (t * 2) % p


for i in range(2, p):
    if i not in two_mults:
        break

t = i
next_mults = []
while t not in next_mults:
    next_mults.append(t)
    t = (t * i) % p

# Because len(next_mults) is 28150 and it contains 2 then it is the primitive
