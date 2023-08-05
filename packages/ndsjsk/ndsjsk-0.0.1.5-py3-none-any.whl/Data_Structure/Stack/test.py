import sys

S = set(map(float, sys.stdin.readline().split()))
A = {k for k in range(-999999, 999999)}
print(A - S)