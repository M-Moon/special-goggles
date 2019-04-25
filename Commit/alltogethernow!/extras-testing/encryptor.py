""" encryptor bby """

import random
import math

KEY_SIZE = 1024

def gcd(a, b): # euclidean algorithm for finding gcd
   while a != 0:
      a, b = b, a % b
   return a

def is_prime(n):
   #lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
   #under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
   #of composite numbers from our potential pool without resorting to Rabin-Miller
   lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
   if (n >= 3):
      if (n&1 != 0):
          for p in lowPrimes:
              if (n == p):
                 return True
              if (n % p == 0):
                  return False
          return rabin_miller(n)
   return False
def multiplicative_inverse(e, phi): # finding the multiplicative inverse of two numbers
   d = 0
   x1, x2 = 0, 1
   y1 = 1
   temp_phi = phi

   while e > 0:
     temp1 = temp_phi/e
     temp2 = temp_phi - temp1 * e
     temp_phi = e
     e = temp2
     
     x = x2- temp1* x1
     y = d - temp1 * y1
     
     x2 = x1
     x1 = x
     d = y1
     y1 = y

   if temp_phi == 1:
     return d + phi

def rabin_miller(n): # rabin-miller method for determining primality on large numbers
   s = n-1
   t = 0
   while s & 1 == 0:
      s = round(s/2)
      t +=1
   k = 0
   while k<128:
      a = random.randrange(2,n-1)
      v = pow(a,s,n) # where values are (num,exp,mod)
      if v != 1:
          i=0
          while v != (n-1):
              if i == t-1:
                  return False
              else:
                  i = i+1
                  v = (v**2)%n
      k+=2
   return True

def generate_large_prime(k):
   # k is the desired bit length
   r=100*(math.log(k,2)+1) # number of attempts max
   r_ = r
   while r>0:
      n = random.randrange(2**(k-1),2**(k))
      r-=1
      if is_prime(n) == True:
          return n
   return "Failure after", r_, "tries."

### actual functions below ###

def generate_keypair(): # generating the keypairs
   p = generate_large_prime(1024)
   q = generate_large_prime(1024)

   while not (isinstance(p, int) and isinstance(q, int)): # if generation has failed
      p = generate_large_prime(1024)
      q = generate_large_prime(1024)
   
   while p == q: # cannot use the two same primes
     q = generate_large_prime(1024)

   # n = pq
   n = p * q

   # Phi is the totient of n
   phi = (p-1) * (q-1)

   # Choose an integer e such that e and phi(n) are coprime
   e = random.randrange(1, phi)

   # Use Euclid's Algorithm to verify that e and phi(n) are comprime
   g = gcd(e, phi)
   while g != 1:
     e = random.randrange(1, phi)
     g = gcd(e, phi)

   # Use Extended Euclid's Algorithm to generate the private key
   d = multiplicative_inverse(e, phi)

   # Return public and private keypair
   # Public key is (e, n) and private key is (d, n)
   return ((e, n), (d, n))

def encrypt(pk, plaintext):
   #Unpack the key into it's components
   key, n = pk
   #Convert each letter in the plaintext to numbers based on the character using a^b mod m
   cipher = [(ord(char) ** key) % n for char in plaintext]
   #Return the array of bytes
   return cipher

def decrypt(pk, ciphertext):
   #Unpack the key into its components
   key, n = pk
   #Generate the plaintext based on the ciphertext and key using a^b mod m
   plain = [chr((char ** key) % n) for char in ciphertext]
   #Return the array of bytes as a string
   return ''.join(plain)

pub_key, priv_key = generate_keypair()

encrypted = encrypt(priv_key, "Hello there me old chum")

print(encrypted)
print("-"*64)

decrypted = decrypt(pub_key, encrypted)

print(decrypted)
