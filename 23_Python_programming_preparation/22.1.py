import functools


@functools.lru_cache(10000)
def judge(n):
    if n < 3:
        return True
    for i in range(3, int(n**0.5)):
        if n % i == 0:
            return False
    return True


@functools.lru_cache(100)
def find_n(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    if not n & 1:
        return find_n(n >> 1) + 1
    div = 3
    while n % div and not judge(div):
        div += 2
    n //= div
    return find_n(n) + 1


if __name__ == '__main__':
    print(find_n(15))
    print(find_n(20))
