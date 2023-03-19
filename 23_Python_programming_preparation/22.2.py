def three(li: list):
    ans = 0
    n = len(li)
    for i in range(0, n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if li[i] > li[j] + 1 > li[k] + 1:
                    ans += 1
    return ans


if __name__ == '__main__':
    print(three([1, 8, 5, 3, 4]))
    print(three([1, 2, 3, 4, 5, 6, 7]))
