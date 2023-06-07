from dataclasses import dataclass

@dataclass
class Bucket:
    __slots__ = ("A", "B", "C")

    A: int
    B: int
    C: int

class Bucket2:
    
    __slots__ = ("A", "B", "C")

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

import time

trials = 10000000

t0 = time.time()
for i in range(trials):
    Bucket(A=i, B=i, C=i)
print(time.time() - t0)

t0 = time.time()
for i in range(trials):
    Bucket2(A=i, B=i, C=i)
print(time.time() - t0)
