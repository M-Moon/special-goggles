import random
import math

'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi): # finding the multiplicative inverse of two numbers
   def extended_gcd(k, j):
      last_remainder, remainder = abs(k), abs(j)
      x, lastx, y, lasty = 0, 1, 1, 0

      while remainder:
         last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)
         x, lastx = lastx - quotient*x, x
         y, lasty = lasty - quotient*y, y
      return last_remainder, lastx * (-1 if k < 0 else 1), lasty * (-1 if j < 0 else 1)

   g, x, y = extended_gcd(e, phi)
   if g != 1:
      print("No multiplicative inverse")
   return x % phi

'''
Tests to see if a number is prime.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
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
   return "Failed"

def generate_keypair(): # generating the keypairs
   p = generate_large_prime(8)
   q = generate_large_prime(8)

   while not (isinstance(p, int) and isinstance(q, int)): # if generation has failed
      p = generate_large_prime(8)
      q = generate_large_prime(8)
      x = 1
   
      while p == q: # cannot use the two same primes
        q = generate_large_prime(8)

   # n = pq
   n = p * q

   # Phi is the totient of n
   phi = (p-1) * (q-1)

   # Choose an integer e such that e and phi(n) are coprime
   e = random.randrange(1, phi)

   # Use Euclid's Algorithm to verify that e and phi(n) are comprime
   #print(e, phi)
   g = gcd(e, phi)
   while g != 1:
     e = random.randrange(1, phi)
     g = gcd(e, phi)

   # Use Extended Euclid's Algorithm to generate the private key
   d = multiplicative_inverse(e, phi)
   #print(d)

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
    

if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print("RSA Encrypter/ Decrypter")
    #p = int(input("Enter a prime number (17, 19, 23, etc): "))
    #q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair()
    print("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(public, message)
    print("Your encrypted message is: ")
    print(encrypted_msg)
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public ," . . .")
    print("Your message is:")
    print(decrypt(private, encrypted_msg))
