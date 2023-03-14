import collections
import random


def check(l: [int]) -> bool:
    d = collections.Counter(l)
    for i in sorted(l):
        if d.get(i + 1) and d.get(i + 2) and d.get(i + 3) and d.get(i + 4):
            return True
    return False


if __name__ == '__main__':
    n = int(input())
    c = 0
    for i in range(n):
        l = [int(random.random() * n) for _ in range(n)]
        if check(l):
            c += 1
    print(c, n)
