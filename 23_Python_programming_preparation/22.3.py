def combine(s: str, k: int):
    ans = []
    n = len(s)

    def dfs(pos, st):
        if len(st) >= k and st not in ans:
            ans.append(st)
        if pos == n:
            return
        if not st or ord(s[pos]) > ord(st[-1]):
            dfs(pos + 1, st + s[pos])
        dfs(pos + 1, st)
    dfs(0, '')
    return ans


if __name__ == '__main__':
    print(combine('abca', 2))
