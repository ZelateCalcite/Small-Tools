from data_check import Check
from collections import defaultdict
from excel_process import Operator
from datetime import datetime

base_dict = {
    # 组织信息
    '组织类型': ['机构部门', '小组'],
    # 企业信息
    '企业类型': ['合资', '独资', '国有', '私营', '全民所有制', '集体所有制', '股份制', '有限责任'],
    '企业状态': ['在业', '存续', '迁入', '迁出', '停业', '注销', '吊销', '清算'],
    '所属行业': ['农、林、牧、渔业', '采矿业', '制造业', '电力、燃气及水的生产和供应业', '建筑业', '交通运输、仓储和邮政业',
                 '信息传输、计算机服务和软件业', '批发和零售业', '住宿和餐饮业', '金融业', '房地产业',
                 '租赁和商务服务业', '科学研究、技术服务和地质勘查业', '水利、环境和公共设施管理业',
                 '居民服务和其他服务业', '教育', '卫生、社会保障和社会福利业', '文化、体育和娱乐业'],
    '纳税人资质': ['一般纳税人', '小规模纳税人'],
    # 新型农业经营主体
    '主体类型': ['龙头企业', '专业大户', '家庭农场', '合作社'],
    # 党员信息
    '文化程度': ['研究生', '（大学）本科', '专科教育（大专）', '中等职业教育（中专）', '普通高级中学教育(高中)',
                 '初级中学教育（初中）', '小学教育（小学）', '文盲或半文盲', '其他'],
    '政治面貌': ['中共党员', '中共预备党员'],
    '职务': ['村支部书记', '村党委副书记', '村委委员', '普通党员', '党委委员'],
    # 项目管理
    '项目类别': ['乡村建设', '产业发展'],
    '项目状态': ['未开始', '进行中', '已完成'],
    # 租赁管理
    '合同类型': ['租赁', '签证'],
    '合同状态': ['初始', '生效', '超期', '失效'],
    '结算方式': ['一次性', '月付', '季付', '半年付', '年付', '其他'],
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
    # 读入excel单元格必须设置为日期格式
    # 读入数据类型为datetime.datetime()
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            if not isinstance(i['value'], datetime):
                fill('type', i)
                continue
            temp = str(i['value'])[:10].split('-')
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


def xmgl(data: dict):
    miss_check(data['项目名称'][1:])
    dict_check(data['项目类别'][1:], '项目类别', True)
    miss_check(data['项目内容'][1:])
    int_check(data['投资金额（万元）'][1:], True)
    dict_check(data['项目状态'][1:], '项目状态', True)
    date_check(data['开始日期'][1:], True)
    date_check(data['立项日期'][1:])
    date_check(data['招投标日期'][1:])
    date_check(data['开工日期'][1:])
    date_check(data['竣工日期'][1:])
    date_check(data['送审日期'][1:])
    date_check(data['结束日期'][1:])

    return {
        'export': data
    }


def mqrj():
    pass


def zlgl(data: dict):
    int_check(data['序号'][1:], True)
    uniq_check(data['合同编号'][1:], True)
    miss_check(data['合同名称'][1:])
    dict_check(data['合同类型'][1:], '合同类型', True)
    dict_check(data['合同状态'][1:], '合同状态', True)
    int_check(data['合同总金额（元）'][1:], True)
    dict_check(data['结算方式'][1:], '结算方式', True)
    date_check(data['签订日期'][1:], True)
    date_check(data['生效日期'][1:], True)
    date_check(data['到期日期'][1:], True)
    miss_check(data['合同甲方'][1:])
    phone_check(data['甲方联系电话'][1:], True)
    miss_check(data['合同乙方'][1:])
    phone_check(data['乙方联系电话'][1:], True)
    phone_check(data['监理联系电话'][1:])
    phone_check(data['成交人联系电话'][1:])
    pid_check(data['成交人证件号'][1:])
    int_check(data['成交人银行卡号'][1:])
    int_check(data['付款期数'][1:], True)
    date_check(data['计划付款日期'][1:], True)
    int_check(data['本期应付金额(元)'][1:], True)
    date_check(data['实际付款日期'][1:])
    int_check(data['本期已付金额（元）'][1:])

    return {
        'export': data
    }


if __name__ == '__main__':
    path = {'./tests/import/1组织信息_导入模板.xlsx': zzxx,
            './tests/import/7企业信息_导入模板.xlsx': qyxx,
            './tests/import/8新型农业经营主体_导入模板.xlsx': xxnyjyzt,
            './tests/import/9厂房信息_导入模板.xlsx': cfxx,
            './tests/import/11党员信息_导入模板.xlsx': dyxx,
            './tests/import/12项目管理_导入模板.xlsx': xmgl,
            './tests/import/14租赁管理_导入模板.xlsx': zlgl}
    for k, f in path.items():
        operator = Operator()
        operator.import_excel(k)
        rtn = f(operator.import_data)
        # print(rtn)
        operator.export_data = rtn['export']
        operator.export_excel(filename=('./tests/export/test' + k.split('/')[-1]))
        # print(rtn['checked'])
