from os import listdir
from re import compile, sub, match
from functools import cmp_to_key


class ReadDir:
    def __init__(self, path, suffix, sort_dict=None, sort_process=None):
        self.sort_process = sort_process
        self.sort_dict = sort_dict
        self.file_list = self.__read_files(path, suffix)

    def __cmp(self, a, b):
        if self.sort_process:
            a, b = self.sort_process(a), self.sort_process(b)
        if self.sort_dict.get(a):
            a = self.sort_dict[a]
        else:
            a = float('inf')
        if self.sort_dict.get(b):
            b = self.sort_dict[b]
        else:
            b = float('inf')
        return 1 if a > b else -1 if a < b else 0

    def __read_files(self, path: str, suffix: str) -> [str]:
        path = sub('/$', '', path)
        suffix = sub(r'^\.', '', suffix)
        files = listdir(path)
        pattern = compile(r'.*\.' + suffix + '$')
        result = []
        for file in files:
            if match(pattern, file) and self.__access_file('{0}/{1}'.format(path, file)):
                result.append('{0}/{1}'.format(path, file))
        result.sort(key=cmp_to_key(self.__cmp))
        return result

    @staticmethod
    def __access_file(file: str) -> bool:
        try:
            open(file)
            return True
        except BaseException as error:
            print('无法打开 ', file)
            print(error)
            return False


if __name__ == '__main__':
    print(ReadDir('./tests', '.xlsx').file_list)
