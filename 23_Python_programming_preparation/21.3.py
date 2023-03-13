import random


def find(n):
    ans = []
    for i in range(1, n + 1):
        c_1, c_0 = 0, 0
        t = i
        while t > 0:
            if t & 1:
                c_1 += 1
            else:
                c_0 += 1
            t >>= 1
        if c_0 < c_1:
            ans.append(i)
    return ans


if __name__ == '__main__':
    print(find(15))
