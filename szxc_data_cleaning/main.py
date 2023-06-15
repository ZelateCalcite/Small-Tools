from read_dir import ReadDir
from excel_process import Operator
from warnings import simplefilter
from re import search, sub
from custom_check import zzxx, hjrk, jtfw, czfjtfw, czffjtfw, xsm, qyxx, xxnyjyzt, cfxx, tdxx, dyxx, xmgl, mqrj, zlgl
from traceback import print_exc
from io import StringIO

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
relations = {
    '组织信息': None,
    '户籍人口': ['组织信息'],
    '家庭房屋': ['户籍人口'],
    '出租房（家庭房屋）': ['家庭房屋'],
    '出租房（非家庭房屋）': ['出租房（家庭房屋）'],
    '新市民': ['出租房（家庭房屋）', '出租房（非家庭房屋）'],
    '企业信息': None,
    '新型农业经营主体': None,
    '厂房信息': None,
    '土地信息': ['户籍人口'],
    '党员信息': None,
    '项目管理': None,
    '民情日记': ['组织信息', '户籍人口'],
    '租赁管理': None
}
public_data = {}


def check_relation_file(key: str, raw: dict, related: dict) -> (bool, str):
    if related.get(key) is None:
        return True, ''
    else:
        miss = []
        valid = True
        for i in related.get(key):
            if raw.get(i) is None:
                valid = False
                miss.append(i)
            else:
                v, m = check_relation_file(i, raw, related)
                valid &= v
                if m != '':
                    miss.append(m)
        temp = ''
        if miss:
            temp = key + ': 缺失' + ', '.join(miss) + '.'
        return valid, temp


def data_reg(filepath: str) -> str:
    fd = {
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
    temp = search(r'[^/]*\.xlsx$', filepath)
    filename = sub(r'\)', '）', sub(r'\(', '（', temp.string[temp.regs[0][0]:temp.regs[0][1]]))
    filetype = ''
    for key in fd.keys():
        if search(key + '_', filename) is not None:
            filetype = key
            break
    return filetype


def check_value(filename, operator):
    funcs = {
        '组织信息': zzxx,
        '户籍人口': hjrk,
        '家庭房屋': jtfw,
        '出租房（家庭房屋）': czfjtfw,
        '出租房（非家庭房屋）': czffjtfw,
        '新市民': xsm,
        '企业信息': qyxx,
        '新型农业经营主体': xxnyjyzt,
        '厂房信息': cfxx,
        '土地信息': tdxx,
        '党员信息': dyxx,
        '项目管理': xmgl,
        '民情日记': mqrj,
        '租赁管理': zlgl
    }
    fun = funcs[filename]
    if filename == '组织信息':
        rtn = fun(operator.import_data)
        public_data.update({'小组': rtn['checked']['组织名称']})
    elif filename == '户籍人口':
        rtn = fun(operator.import_data, public_data['小组'])
        public_data.update({
            '门牌号': rtn['checked']['门牌号'],
            '户主姓名': rtn['checked']['姓名'],
            '身份证号': rtn['checked']['身份证号']
        })
    elif filename == '家庭房屋':
        rtn = fun(operator.import_data, public_data['门牌号'])
        public_data.update({
            '家庭门牌号': rtn['checked']['门牌号'],
            '家庭房屋编号': rtn['checked']['房屋编号']
        })
    elif filename == '出租房（家庭房屋）':
        rtn = fun(operator.import_data, {'门牌号': public_data['家庭门牌号'], '房屋编号': public_data['家庭房屋编号']})
        public_data.update({
            '出租房家庭门牌号': rtn['checked']['门牌号'],
            '出租房家庭房屋编号': rtn['checked']['房屋编号']
        })
    elif filename == '出租房（非家庭房屋）':
        rtn = fun(operator.import_data, {'门牌号': public_data['出租房家庭门牌号'], '房屋编号': public_data['出租房家庭房屋编号']})
        public_data.update({
            '出租房非家庭门牌号': rtn['checked']['门牌号']
        })
    elif filename == '新市民':
        temp = {}
        temp.update(public_data['出租房家庭门牌号'])
        temp.update(public_data['出租房非家庭门牌号'])
        rtn = fun(operator.import_data, temp)
    elif filename == '土地信息':
        rtn = fun(operator.import_data, public_data['身份证号'])
    elif filename == '民情日记':
        rtn = fun(operator.import_data, {'小组': public_data['小组'], '身份证号': public_data['身份证号']})
    else:
        rtn = fun(operator.import_data)
    return rtn['export']


def main():
    files = ReadDir('./tests/real', '.xlsx', file_sort, data_reg).file_list
    all_data = {}
    available = {}

    for index, filepath in enumerate(files):
        operator = Operator()
        filetype = data_reg(filepath)
        if filetype != '':
            operator.export_data = operator.import_excel(filepath)
            if all_data.get(filetype) is None:
                all_data[filetype] = operator
            else:
                print('存在重复{0}模板'.format(filetype))
                return -10002

    if len(all_data) == 0:
        print('===\t未读取到文件 请检查文件模板命名和文件后缀名\t===')
        return -10000

    print('===\t正在检查文件关联性\t===')
    for key in all_data.keys():
        v, m = check_relation_file(key, all_data, relations)
        if not v:
            print(m)
        else:
            available.update({key: all_data[key]})
    if len(available) == len(all_data):
        print('无关联文件缺失\n')

    if len(available) == 0:
        print('===\t无可校验文件\t===')
        return -10001

    print('===\t已读入数据\t===')
    for i in available.keys():
        print(i)
    print('===\t开始处理\t===')
    fp = StringIO()

    for filename, filedata in available.items():
        try:
            filedata.export_data = check_value(filename, filedata)
            filedata.export_excel(filename=filename+'_导出模板.xlsx')
        except BaseException as error:
            print('\033[91m发生错误: \033[0m' + filename + '_导入模板, ', end='')
            print(error)
            print_exc(file=fp)

    wrong_info = fp.getvalue()
    if wrong_info:
        print('\n\033[93m详细错误信息\033[0m')
        print(fp.getvalue())

    print('===\t处理完成\t===')
    return 0


main()
input('按下Enter键退出')
