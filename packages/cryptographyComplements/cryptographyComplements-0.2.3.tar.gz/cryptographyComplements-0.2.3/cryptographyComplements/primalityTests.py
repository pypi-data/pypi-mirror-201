from cryptographyComplements.tools import Numbers
def EulerTotientPrimalityTest(n: int):
    "Using the equation: p - 1 = phi(p), you can verify if a number is prime. \nThis primality test is deterministic but numbers greater than 2^60 requires to much time, and computational power, to be calculated using this primality test."

    from cryptographyComplements.mathFunctions import EulerTotientFunction

    if not isinstance(n, int) and not isinstance(n, float):
        return None

    elif int(n) < 0: # verifying if the input belongs to N
        return False

    n = int(n)
    if n == 5 or n==2: # needs to be put because in the if condition below it would be set to false
        return True
    
    elif Numbers.isEven(n) or str(n).endswith("5"): # skip the nums that are not prime
        return False

    phi = EulerTotientFunction(n)

    if (n - 1) == phi:
        return True
    
    return False

class MersennePrimePrimalityTest:
    def LucasPrimalityTest(number:int):
        "This primality test is probabilistic, and is valid only for Mersenne numbers, if the functions returns false it's sure not a prime number but if it returns True then it could be a pseudoprime."
        
        from cryptographyComplements.mathFunctions import MersennePrime

        lucasNumbers = MersennePrime.LucasNumbers(number)

        x = (lucasNumbers[number-1] - 1) / number

        if x.is_integer():
            return True
        
        return False
    

    def LucasLehmerPrimalityTest(power:int):
        "This primality test is deterministic, and is valid only for Mersenne numbers, to check whether a number is prime or not."

        from cryptographyComplements.mathFunctions import MersennePrime

        mersenne = (2**power) - 1 # we set this here, because we now have only to calculate it a single time

        lucaslehmerSequence = MersennePrime.LucasLehmerModuloNumbers(power-1, mersenne)

        x = lucaslehmerSequence[power-2] / mersenne

        if x.is_integer():
            return True
        
        return False
    
def FermatPrimalityTest(p:int, a:int):
    "From a given number and an integer, check if the number is prime. The Fermat Primality test is probabilistic."
    from cryptographyComplements import EuclideanAlgorithm, FermatLittleTheorem

    if EuclideanAlgorithm(p, a) != 1:
        return False
    
    if FermatLittleTheorem(a, p) == 1:
        return True
    
    return False