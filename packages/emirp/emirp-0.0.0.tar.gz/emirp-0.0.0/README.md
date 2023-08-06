# Emirp Generator:
This program will generate Emrip primes with an iterator.

## Usage:
```python
from emirp import get_emirps

if __name__ == '__main__':
    a = get_emirps()

    for i in range(10000):
    
        print(next(a))
```

This program uses my other library "getprimes" for calculating primes.
