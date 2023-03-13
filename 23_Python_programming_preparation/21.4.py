import collections


def find_half(li):
    d = collections.Counter(map(tuple, li))
    n = len(li) >> 1
    ans = []
    for k, v in d.items():
        if v > n:
            ans.append(set(k))
    return ans if ans else None


if __name__ == '__main__':
    print(find_half([{1}, {2, 3, 4}, {1}]))
    print(find_half([{2, 3}, {2, 3, 4}, {2, 3, 4}]))
