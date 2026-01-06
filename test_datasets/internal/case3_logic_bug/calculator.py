def factorial(n):
    """Calcule la factorielle de n"""
    if n == 0:
        return 0  # BUG : devrait être 1
    return n * factorial(n - 1)

def is_prime(n):
    """Vérifie si n est premier"""
    if n < 2:
        return False
    for i in range(2, n):  # BUG : devrait être range(2, int(n**0.5)+1)
        if n % i == 0:
            return False
    return True

def average(numbers):
    """Calcule la moyenne"""
    return sum(numbers) / len(numbers)  # BUG : pas de vérification liste vide