from os import listdir
from re import compile, sub, match


class ReadDir:
    def __init__(self, path, suffix):
        self.file_list = self.__read_files(path, suffix)

    def __read_files(self, path: str, suffix: str) -> [str]:
        path = sub('/$', '', path)
        suffix = sub(r'^\.', '', suffix)
        files = listdir(path)
        pattern = compile(r'.*\.' + suffix + '$')
        result = []
        for file in files:
            if match(pattern, file) and self.__access_file('{0}/{1}'.format(path, file)):
                result.append('{0}/{1}'.format(path, file))
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
