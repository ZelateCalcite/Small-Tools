import os
import re


def get_dir_files(path: str) -> [str]:
    return os.listdir(path)


def read_file(path: str, files: [str], suffix: str) -> [classmethod]:
    rtn = []
    if not suffix:
        suffix = '.+'
    for file in files:
        if re.search(re.compile(r'.\.' + suffix + '$'), file):
            rtn.append((open(path + '/' + file, mode='r', encoding='utf-8'), file))
    return rtn


def search_dir_content(pattern: str, path: str) -> []:
    # 相对路径转换为绝对路径
    # 手写转换，用os.path.realpath()代替
    # if re.search(r'^\./.*$', path):
    #     path = re.sub(r'^\./', re.sub(r'\\', '/', os.getcwd()) + '/', path)
    path = re.sub(r'\\', '/', os.path.realpath(path))
    result = []
    file_names = get_dir_files(path)
    search_pattern = re.compile(pattern)
    files = read_file(path, file_names, '')
    for file, name in files:
        if re.search(search_pattern, file.read()):
            result.append(path + '/' + name)
    print(result)


if __name__ == '__main__':
    search_dir_content('1.1.1', 'D:/stable-diffusion-webui')
