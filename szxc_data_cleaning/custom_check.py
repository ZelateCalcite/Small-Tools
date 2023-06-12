from data_check import Check
from collections import defaultdict
from excel_process import Operator

base_dict = {
    '组织类型': ['机构部门', '小组'],
    '企业类型': ['合资', '独资', '国有', '私营', '全民所有制', '集体所有制', '股份制', '有限责任'],
    '企业状态': ['在业', '存续', '迁入', '迁出', '停业', '注销', '吊销', '清算'],
    '所属行业': ['农、林、牧、渔业', '采矿业', '制造业', '电力、燃气及水的生产和供应业', '建筑业', '交通运输、仓储和邮政业',
                 '信息传输、计算机服务和软件业', '批发和零售业', '住宿和餐饮业', '金融业', '房地产业',
                 '租赁和商务服务业', '科学研究、技术服务和地质勘查业', '水利、环境和公共设施管理业',
                 '居民服务和其他服务业', '教育', '卫生、社会保障和社会福利业', '文化、体育和娱乐业'],
    '纳税人资质': ['一般纳税人', '小规模纳税人'],
    '主体类型': ['龙头企业', '专业大户', '家庭农场', '合作社'],
    '文化程度': ['研究生', '（大学）本科', '专科教育（大专）', '中等职业教育（中专）', '普通高级中学教育(高中)',
                 '初级中学教育（初中）', '小学教育（小学）', '文盲或半文盲', '其他'],
    '政治面貌': ['中共党员', '中共预备党员'],
    '职务': ['村支部书记', '村党委副书记', '村委委员', '普通党员', '党委委员']
}
check = Check(base_dict)


def int_check(data: list, require=False):
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            if not type_number(i['value']):
                fill('type', i)
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)


def uniq_check(data: list, require=False):
    temp = defaultdict(int)
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            temp[i['value']] += 1
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)
    for i in data:
        try:
            if not check.uniq_check(temp, i['value']):
                fill('uniq', i)
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)


def pid_check(data: list, require=False, unique=False):
    uniq = defaultdict(int)
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            temp = check.pid_check(i['value'])
            if temp == 'wrong character':
                fill('type', i)
            elif temp == 'wrong length':
                fill('leng', i)
            elif temp != 'checked':
                fill('date', i)
            else:
                uniq[i['value']] += 1
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)
    if unique:
        for i in data:
            try:
                if not check.uniq_check(uniq, i['value']):
                    fill('uniq', i)
            except BaseException as error:
                print('error:')
                print(error)
                fill('error', i)


def dict_check(data: list, name: str,  require=False):
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            if not check.dict_check(name, i['value']):
                fill('dict', i)
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)


def date_check(data: list, require=False):
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            temp = i['value'].split('/')
            if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
                if type_number(temp[0]) and type_number(temp[1]) and type_number(temp[2]):
                    stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
                    if stat == 'checked':
                        i['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
                        continue
            fill('date', i)
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)


def miss_check(data: list):
    for i in data:
        try:
            if i['value'] is None:
                fill('miss', i)
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)


def phone_check(data: list, require=False):
    for i in data:
        try:
            if i['value'] is not None:
                stat = check.phone_check(i['value'])
                if stat == 'wrong length':
                    fill('leng', i)
                elif stat == 'wrong character':
                    fill('type', i)
            else:
                if require:
                    fill('miss', i)
        except BaseException as error:
            print('error:')
            print(error)
            fill('error', i)


def checked(data: dict, name: str):
    result = {}
    wrong = defaultdict(int)
    for key in data.keys():
        for i in data[key]:
            if i['style'].fill.fgColor.rgb != '00FFFFFF':
                wrong[i['row']] += 1
    for i in data[name][1:]:
        if wrong.get(i['row']) is None:
            result.update({i['value']: 1})
    return result


def fill(fill_type: str, cell: dict):
    colors = {
        'date': 'FFFF00',
        'dict': 'B0E0E6',
        'miss': '00FF00',
        'type': 'A020F0',
        'uniq': '00FFFF',
        'leng': '0000FF',
        'mult': 'FF0000',
        'error': 'F0FFF0'
    }
    cell['style'].set_fill(colors[fill_type])


def type_number(obj: int | str) -> bool:
    return isinstance(obj, int) or obj.isdigit()


def zzxx(data: dict) -> dict:

    int_check(data['序号'][1:], True)

    miss_check(data['组织名称'][1:])

    dict_check(data['组织类型'][1:], '组织类型', True)

    int_check(data['排序序号'][1:])

    phone_check(data['联系电话'][1:])

    return {
        'export': data,
        'checked': checked(data, '组织名称')
    }


def hjrk():
    pass


def jtfw():
    pass


def czfjtfw():
    pass


def czffjtfw():
    pass


def xsm():
    pass


def qyxx(data: dict) -> dict:
    int_check(data['序号'][1:], True)

    uniq_check(data['企业名称'][1:], True)

    uniq_check(data['统一社会信用代码'][1:])

    uniq_check(data['门牌号'][1:], True)

    dict_check(data['企业类型'][1:], '企业类型', True)

    dict_check(data['企业状态'][1:], '企业状态', True)

    miss_check(data['法人代表'][1:])

    date_check(data['成立日期'][1:], True)

    int_check(data['注册资本（万）'][1:], True)

    miss_check(data['注册地址'][1:])

    date_check(data['入驻日期'][1:], True)

    date_check(data['迁出日期'][1:])

    dict_check(data['所属行业'][1:], '所属行业')

    int_check(data['实缴资本（万）'][1:])

    date_check(data['核准日期'][1:])

    dict_check(data['纳税人资质'][1:], '纳税人资质')

    phone_check(data['联系电话'][1:])

    int_check(data['占地面积（亩）'][1:], True)

    return {
        'export': data
    }


def xxnyjyzt(data: dict) -> dict:
    int_check(data['序号'][1:], True)

    miss_check(data['主体名称'][1:])

    dict_check(data['主体类型'][1:], '主体类型', True)

    miss_check(data['产业'][1:])

    miss_check(data['法人'][1:])

    phone_check(data['联系电话'][1:])

    return {
        'export': data
    }


def cfxx(data: dict) -> dict:
    int_check(data['序号'][1:], True)

    uniq_check(data['厂房名称'][1:], True)

    int_check(data['建筑面积(m²)'][1:], True)

    date_check(data['建造日期'][1:], True)

    date_check(data['拆除日期'][1:])

    miss_check(data['联系人'][1:])

    phone_check(data['联系电话'][1:])

    return {
        'export': data
    }


def tdxx():
    pass


def dyxx(data: dict):
    int_check(data['序号'][1:], True)

    miss_check(data['姓名'][1:])

    pid_check(data['身份证号'][1:], True, True)

    dict_check(data['文化程度'][1:], '文化程度', True)

    phone_check(data['联系电话'][1:])

    dict_check(data['政治面貌'][1:], '政治面貌', True)

    miss_check(data['所属党组织'][1:])

    date_check(data['入党日期'][1:], True)

    date_check(data['转入日期'][1:])

    dict_check(data['职务'][1:], '职务')

    return {
        'export': data
    }


def xmgl():
    pass


def mqrj():
    pass


def zlgl():
    pass


if __name__ == '__main__':
    operator = Operator()

    operator.import_excel('./tests/import/1组织信息_导入模板.xlsx')
    # operator.import_excel('./tests/import/7企业信息_导入模板.xlsx')
    # operator.import_excel('./tests/import/8新型农业经营主体_导入模板.xlsx')
    # operator.import_excel('./tests/import/9厂房信息_导入模板.xlsx')
    # operator.import_excel('./tests/import/11党员信息_导入模板.xlsx')

    rtn = zzxx(operator.import_data)
    # rtn = qyxx(operator.import_data)
    # rtn = xxnyjyzt(operator.import_data)
    # rtn = cfxx(operator.import_data)
    # rtn = dyxx(operator.import_data)

    print(rtn)

    operator.export_data = rtn['export']

    operator.export_excel(filename='./tests/export/test组织信息_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test企业信息_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test新型农业经营主体_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test厂房信息_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test党员信息_导入模板.xlsx')

    # print(rtn['checked'])
