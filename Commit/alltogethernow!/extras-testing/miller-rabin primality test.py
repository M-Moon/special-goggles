""" Miller-Rabin Primality Test """

import random

def miller_rabin(n):
    
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    
    # Miller-Rabin test for primality    
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True
 
    for i in range(64):#number of trials 
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True  

primality = False
while not primality:
    n = random.randrange(1000000001, 100000000000000000001)
    primality = miller_rabin(n)
print(n)
print(primality)
