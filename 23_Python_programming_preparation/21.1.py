import random


def find_mul_max(li):
    mul = -float('inf')
    su = -float('inf')
    ans = ()
    li.sort()
    for i in range(len(li)):
        for j in range(i + 1, len(li)):
            if mul <= li[i] * li[j]:
                mul = li[i] * li[j]
                if su < li[i] + li[j]:
                    ans = (li[i], li[j])
                    su = li[i] + li[j]
    return list(ans)


if __name__ == '__main__':
    l = [int(random.random() * 100) * ((-1) ** random.randint(1, 2)) for i in range(10)]
    print(sorted(l))
    print(find_mul_max(l))
