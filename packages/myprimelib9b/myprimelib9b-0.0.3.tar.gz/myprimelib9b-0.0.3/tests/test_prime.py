#from myprimelib9b import is_prime
from myprimelib9b.prime_numbers import is_prime
def test_false():
    assert is_prime(10) is False

def test_true():
    assert is_prime(11) is True
