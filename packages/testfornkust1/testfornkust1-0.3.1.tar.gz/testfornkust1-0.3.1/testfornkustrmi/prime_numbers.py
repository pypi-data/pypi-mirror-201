import math

def _divides(div, n):
    """
    returns True if and only if div divides n which is equivalent to
    n = k*div with k an integer.
    """
    return (n % div == 0)

def is_prime(n):
    """Function to evaluate whether an integer is a prime number.
    A prime number is defined as being greater than 1 and is not a product of
    two strictly smaller integers.

    Args: 
        n (int): integer to evaluate

    Returns: 
        bool: whether or not n is a prime number
        
    """
    if type(n) is not int or n <=1:
        # If smaller than 1 or not an integer, it is not a prime number
        return False
    # n is not a prime number if a divisor is found in between 2 and sqrt(n)  
    for div in range(2, math.floor(math.sqrt(n))+1):
        if _divides(div, n):
            return False
    return True