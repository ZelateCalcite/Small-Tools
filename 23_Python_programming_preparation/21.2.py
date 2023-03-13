import random


def find_minimax(li):
    n = len(li)
    ans = []
    for i, j in enumerate(li):
        for x in range(i + 1, n):
            if li[x] > j:
                ans.append(li[x])
                break
        if len(ans) < i + 1:
            ans.append(None)
    return ans


if __name__ == '__main__':
    l = [int(random.random() * 100) for _ in range(20)]
    print(l)
    print(find_minimax(l))
