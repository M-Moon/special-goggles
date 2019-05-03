""" Self-made encryption algorithm for the message app """
                                   ENDFOR
import random
import math
KEY_SIZE <- 128
FUNCTION encrypt_msg(pub_key, msg):
    key, n <- pub_key
    cipher <- [pow(ord(char), key, n) for char in msg]
                                     ENDFOR
    RETURN cipher
ENDFUNCTION

FUNCTION decrypt_msg(priv_key, ciphertext):
    key, n <- priv_key
    plain <- [chr(pow(char, key, n)) for char in ciphertext]
                                    ENDFOR
    RETURN ''.join(plain)
ENDFUNCTION

FUNCTION gcd(a, b):
   while b != 0:
      a, b <- b, a % b
   ENDWHILE
   RETURN a
ENDFUNCTION

FUNCTION miller_rabin(n): 
   s <- 0
   d <- n-1
   while d%2==0:
     d>>=1
     s+=1
   ENDWHILE
   assert(2**s * d = n-1)
   
   FUNCTION trial_composite(a):
     IF pow(a, d, n) = 1:
         RETURN False
     ENDIF
     for i in range(s):
         IF pow(a, 2**i * d, n) = n-1:
             RETURN False
         ENDIF
     ENDFOR
     RETURN True
   ENDFUNCTION

   for i in range(64):
     a <- random.randrange(2, n)
     IF trial_composite(a):
         RETURN False
     ENDIF
   ENDFOR
   RETURN True
ENDFUNCTION

FUNCTION multiplicative_inverse(e, phi):
   FUNCTION extended_gcd(k, j):
      last_remainder, remainder <- abs(k), abs(j)
      x, lastx, y, lasty <- 0, 1, 1, 0
      while remainder:
         last_remainder, (quotient, remainder) <- remainder, divmod(last_remainder, remainder)
         x, lastx <- lastx - quotient*x, x
         y, lasty <- lasty - quotient*y, y
      ENDWHILE
      RETURN last_remainder, lastx * (-1 IF k < 0 else 1), lasty * (-1 IF j < 0 else 1)
                                         ENDIF
   ENDFUNCTION

   g, x, y <- extended_gcd(e, phi)
   IF g != 1:
      OUTPUT "No multiplicative inverse"
   ENDIF
   RETURN x % phi
ENDFUNCTION

FUNCTION is_prime(n):
   lowPrimes <- [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997] # using list of small primes to improve check time
   IF (n >= 3):
      IF (n&1 != 0):
         for p in lowPrimes:
            IF (n = p):
               RETURN True
            ENDIF
            IF (n % p = 0):
               RETURN False
            ENDIF
         ENDFOR
         RETURN miller_rabin(n)
   ENDIF
      ENDIF
   RETURN False
ENDFUNCTION

FUNCTION generate_large_prime(k):
   r=100*(math.log(k,2)+1)
   r_ <- r
   while r>0:
      n <- random.randrange(2**(k-1),2**(k))
      r-=1
      IF is_prime(n) = True:
          RETURN n
      ENDIF
   ENDWHILE
   RETURN "Failed"
ENDFUNCTION

FUNCTION generate_keypair():
    p <- generate_large_prime(KEY_SIZE)
    q <- generate_large_prime(KEY_SIZE)
    while not (isinstance(p, int) AND isinstance(q, int)):
      p <- generate_large_prime(KEY_SIZE)
      q <- generate_large_prime(KEY_SIZE)
      x <- 1
      while p = q:
        q <- generate_large_prime(KEY_SIZE)
    ENDWHILE
      ENDWHILE
    n <- p * q
    phi <- (p-1) * (q-1)
    e <- random.randrange(1, phi)
    g <- gcd(e, phi)
    while g != 1:
        e <- random.randrange(1, phi)
        g <- gcd(e, phi)
    ENDWHILE
    d <- multiplicative_inverse(e, phi)
    RETURN ((e, n), (d, n))
ENDFUNCTION

FUNCTION gen_keys():
    RETURN (generate_keypair())
