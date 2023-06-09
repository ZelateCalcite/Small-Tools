from read_dir import ReadDir
from excel_process import Operator
from warnings import simplefilter
from re import search, sub

simplefilter('ignore')


file_sort = {
    '组织信息': 1,
    '户籍人口': 2,
    '家庭房屋': 3,
    '出租房（家庭房屋）': 4,
    '出租房（非家庭房屋）': 5,
    '新市民': 6,
    '企业信息': 7,
    '新型农业经营主体': 8,
    '厂房信息': 9,
    '土地信息': 10,
    '党员信息': 11,
    '项目管理': 12,
    '民情日记': 13,
    '租赁管理': 14
}


def check_value(file, data):
    pass


def main():
    files = ReadDir('./tests/import', '.xlsx').file_list
    all_data = {}
    checked_data = {}

    for index, filepath in enumerate(files):
        operator = Operator()
        temp = search(r'[^/]*\.xlsx$', filepath)
        filename = sub(r'\)', '）', sub(r'\(', '（', temp.string[temp.regs[0][0]:temp.regs[0][1]]))
        filetype = ''
        for key in file_sort.keys():
            if search(key + '_', filename) is not None:
                filetype = key
                break
        if filetype != '':
            operator.export_data = operator.import_excel(filepath)
            if all_data.get(filetype) is None:
                all_data[filetype] = operator
            else:
                print('存在重复{0}模板'.format(filetype))
                return 10002
    if len(all_data) < len(file_sort):
        print('缺失模板')
        return 10001

    for filename, filedata in all_data.items():
        try:
            for title, cells in filedata.export_data.items():
                check_value(title, cells)
            filedata.export_excel(filename=filename.replace('import', 'export'))
        except BaseException as error:
            print(error)


main()
