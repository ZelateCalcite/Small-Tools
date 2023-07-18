from data_check import Check
from collections import defaultdict
from excel_process import Operator
from datetime import datetime
from re import match

base_dict = {
    # 组织信息
    '组织类型': ['机构部门', '小组'],
    # 户籍人口 Duplicate: '文化程度'
    '与户主关系': ['户主', '配偶', '子', '女', '女婿', '儿媳', '兄弟姐妹', '孙子、孙女或外孙子、外孙女',
                   '祖父母或外祖父母', '父母', '曾孙子、曾孙女或曾外孙子、曾外孙女', '其他亲属', '非亲属'],
    '婚姻状况': ['未婚', '已婚', '初婚', '再婚', '复婚', '丧偶', '离婚', '未说明婚姻状况'],
    '是否常住': ['是', '否'],
    '户口性质': ['农村', '城市'],
    '政治面貌': ['中共党员', '中共预备党员', '共青团员', '民革党员', '民盟盟员', '民建会员', '民进会员', '农工党党员',
                 '致公党党员', '九三学社社员', '台盟盟员', '无党派民主人士', '群众（现称普通公民）'],
    '迁入原因': ['出生', '迁入市（县）外', '其他'],
    '民族': ['阿昌族', '鄂温克族', '傈僳族', '水族', '白族', '高山族', '珞巴族', '塔吉克族', '保安族', '仡佬族', '满族',
             '塔塔尔族', '布朗族', '哈尼族', '毛南族', '土家族', '布依族', '哈萨克族', '门巴族', '土族', '朝鲜族',
             '汉族', '蒙古族', '佤族', '达斡尔族', '赫哲族', '苗族', '维吾尔族', '傣族', '回族', '仫佬族', '乌孜别克族',
             '德昂族', '基诺族', '纳西族', '锡伯族', '东乡族', '京族', '怒族', '瑶族', '侗族', '景颇族', '普米族',
             '彝族', '独龙族', '柯尔克孜族', '羌族', '裕固族', '俄罗斯族', '拉祜族', '撒拉族', '藏族', '鄂伦春族',
             '黎族', '畲族', '壮族', '阿昌', '鄂温克', '傈僳', '水', '白', '高山', '珞巴', '塔吉克', '保安', '仡佬',
             '满', '塔塔尔', '布朗', '哈尼', '毛南', '土家', '布依', '哈萨克', '门巴', '土', '朝鲜', '汉', '蒙古', '佤',
             '达斡尔', '赫哲', '苗', '维吾尔', '傣', '回', '仫佬', '乌孜别克', '德昂', '基诺', '纳西', '锡伯', '东乡',
             '京', '怒', '瑶', '侗', '景颇', '普米', '彝', '独龙', '柯尔克孜', '羌', '裕固', '俄罗斯', '拉祜', '撒拉',
             '藏', '鄂伦春', '黎', '畲', '壮', '其他', '外国血统中国籍人士'],
    # 家庭房屋
    '房屋类别': ['自建房', '公寓房', '商品用房', '新村楼房', '其他'],
    # 出租房非家庭房屋
    '出租房类型': ['企业集宿', '工地', '码头', '学校', '其他'],
    # 新市民
    '与租住人关系': ['租住人', '配偶', '子', '女', '女婿', '儿媳', '兄弟姐妹', '孙子、孙女或外孙子、外孙女',
                     '祖父母或外祖父母', '父母', '其他亲属', '非亲属'],
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
    # 土地信息
    '土地类别': ['自留地', '宅基地', '承包地', '集体建设用地'],
    # 党员信息
    '文化程度': ['研究生', '（大学）本科', '专科教育（大专）', '中等职业教育（中专）', '普通高级中学教育(高中)',
                 '初级中学教育（初中）', '小学教育（小学）', '文盲或半文盲', '其他'],
    '党员政治面貌': ['中共党员', '中共预备党员'],
    '职务': ['村支部书记', '村党委副书记', '村委委员', '普通党员', '党委委员'],
    # 项目管理
    '项目类别': ['乡村建设', '产业发展'],
    '项目状态': ['未开始', '进行中', '已完成'],
    # 民情日记
    '事件类型': ['乡村文明', '关爱弱势群体', '纠纷调解', '投诉建议', '安全生产'],
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
            print('error: int_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
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
            print('error: uniq_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)
    dup = {}
    for i in data:
        try:
            if not check.uniq_check(temp, i['value']):
                fill('uniq', i)
                dup[i['value']] = 1
        except BaseException as error:
            print('error: uniq_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)
    return dup


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
            print('error: pid_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)
    if unique:
        for i in data:
            try:
                if not check.uniq_check(uniq, i['value']):
                    fill('uniq', i)
            except BaseException as error:
                print('error: pid_check')
                print(error)
                print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
                fill('error', i)


def dict_check(data: list, name: str, require=False):
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            if not check.dict_check(name, i['value']):
                fill('dict', i)
        except BaseException as error:
            print('error: dict_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
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
            print('error: date_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)


def miss_check(data: list):
    for i in data:
        try:
            if i['value'] is None:
                fill('miss', i)
        except BaseException as error:
            print('error: miss_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)


def phone_check(data: list, require=False):
    for i in data:
        try:
            if i['value'] is not None:
                stat = check.phone_check(str(i['value']))
                if stat == 'wrong length':
                    fill('leng', i)
                elif stat == 'wrong character':
                    fill('type', i)
            else:
                if require:
                    fill('miss', i)
        except BaseException as error:
            print('error: phone_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)


def year_check(data: list, require=False):
    for i in data:
        try:
            if i['value'] is not None:
                if not type_number(i['value']):
                    fill('type', i)
                    continue
                temp = str(i['value'])
                if not (1900 <= eval(temp) <= 2999):
                    fill('date', i)
            else:
                if require:
                    fill('miss', i)
        except BaseException as error:
            print('error: year_check')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)


def relation_check_outside(data: list, relation: dict, require=False):
    for i in data:
        try:
            if i['value'] is None:
                if require:
                    fill('miss', i)
                continue
            if relation.get(i['value']) is None:
                fill('rela', i)
        except BaseException as error:
            print('error: relation_check_outside')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)


def checked(data: dict, *args):
    result = {}
    wrong = defaultdict(int)
    for key in data.keys():
        for i in data[key]:
            if i['style'].fill.fgColor.rgb != '00FFFFFF':
                wrong[i['row']] += 1
    for name in args:
        temp = {}
        for i in data[name][1:]:
            if wrong.get(i['row']) is None:
                temp.update({i['value']: i['row']})
        result[name] = temp
    return result


def fill(fill_type: str, cell: dict):
    colors = {
        'date': 'FFFF00',
        'dict': 'B0E0E6',
        'miss': '00FF00',
        'type': 'A020F0',
        'uniq': '00FFFF',
        'leng': '0000FF',
        'rela': '8470FF',
        'mult': 'FF0000',
        'error': 'F0FFF0'
    }
    cell['style'].set_fill(colors[fill_type])


def type_number(obj: int | float | str) -> bool:
    if isinstance(obj, int) or isinstance(obj, float):
        obj = str(obj)
    return match(r'^0\.\d+$|^[1-9]\d*\.\d+$|^[1-9]\d*$|^0$', obj) is not None


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


def hjrk(data: dict, relation: dict):
    # no relation
    int_check(data['序号'][1:], True)
    dict_check(data['民族'][1:], '民族', True)
    dict_check(data['婚姻状况'][1:], '婚姻状况')
    dict_check(data['是否常住'][1:], '是否常住', True)
    dict_check(data['文化程度'][1:], '文化程度')
    phone_check(data['联系电话'][1:])
    dict_check(data['政治面貌'][1:], '政治面貌', True)
    date_check(data['迁入日期'][1:])
    uniq_check(data['身份证号'][1:], True)
    miss_check(data['姓名'][1:])

    # outside relation
    relation_check_outside(data['小组'][1:], relation, True)

    # inside relation
    mph = defaultdict(list)
    n1, n2 = len(data['门牌号']), len(data['与户主关系'])
    n = min(n1, n2)
    for i in data['门牌号'][n:]:
        fill('miss', i)
    for i in data['与户主关系'][n:]:
        fill('miss', i)

    rows = {}
    dict_check(data['与户主关系'][1:], '与户主关系', True)
    for i in range(1, n):
        if data['门牌号'][i]['value'] is not None:
            rows.update({i: {
                '门牌号': data['门牌号'][i]['value'],
                '与户主关系': data['与户主关系'][i]['value'],
            }})
        else:
            fill('miss', data['门牌号'][i])

    for row, value in rows.items():
        mph[value['门牌号']].append(value['与户主关系'])
    for i in data['门牌号'][1:]:
        try:
            # 校验关系
            if mph[i['value']].count('户主') != 1:
                fill('mult', i)
        except BaseException as error:
            print('error:')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)

    return {
        'export': data,
        'checked': checked(data, '门牌号', '姓名', '身份证号')
    }


def jtfw(data: dict, relation: dict):
    # no relation
    int_check(data['序号'][1:], True)
    pid_check(data['身份证号'][1:], True, True)
    uniq_check(data['房屋编号'][1:], True)
    dict_check(data['房屋类别'][1:], '房屋类别', True)
    year_check(data['建造年份'][1:], True)
    year_check(data['拆除年份'][1:])
    int_check(data['房屋批准面积（亩）'][1:])
    int_check(data['建筑面积（㎡）'][1:])
    int_check(data['超建面积（㎡）'][1:])
    int_check(data['辅房面积（㎡）'][1:])
    int_check(data['车库面积（㎡）'][1:])
    int_check(data['占地面积（㎡）'][1:])

    # outside relation
    relation_check_outside(data['门牌号'][1:], relation, True)
    uniq_check(data['门牌号'][1:], True)

    return {
        'export': data,
        'checked': checked(data, '房屋编号', '门牌号')
    }


def czfjtfw(data: dict, relation: dict):
    # no relation
    int_check(data['序号'][1:], True)
    pid_check(data['户主身份证号'][1:], True)

    # outside relation
    outside_rows = defaultdict(dict)
    for key, row in relation['房屋编号'].items():
        outside_rows[row].update({'房屋编号': key})
    for key, row in relation['门牌号'].items():
        outside_rows[row].update({'门牌号': key})
    outside_relation = {}
    for i in outside_rows.values():
        outside_relation.update({i['房屋编号']: i['门牌号']})

    inside_rows = defaultdict(dict)
    uniq_check(data['房屋编号'][1:], True)
    uniq_check(data['门牌号'][1:], True)
    for i in data['房屋编号'][1:]:
        if i['style'].fill.fgColor.rgb == '00FFFFFF':
            inside_rows[i['row']].update({'房屋编号': i['value']})
    for i in data['门牌号'][1:]:
        if i['style'].fill.fgColor.rgb == '00FFFFFF':
            inside_rows[i['row']].update({'门牌号': i['value']})
    inside_relation = {}
    for i in inside_rows.values():
        if i.get('房屋编号') is not None and i.get('门牌号') is not None:
            inside_relation.update({i['房屋编号']: i['门牌号']})

    wrong_f, wrong_m = {}, {}
    for i, m in inside_relation.items():
        if outside_relation.get(i) != m:
            wrong_f.update({i: 1})
            wrong_m.update({m: 1})
    for i in data['房屋编号'][1:]:
        try:
            if wrong_f.get(i['value']):
                fill('mult', i)
        except BaseException as error:
            print('error: relation_check_outside')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)
    for i in data['门牌号'][1:]:
        try:
            if wrong_m.get(i['value']):
                fill('mult', i)
        except BaseException as error:
            print('error: relation_check_outside')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)

    return {
        'export': data,
        'checked': checked(data, '房屋编号', '门牌号')
    }


def czffjtfw(data: dict, relation: dict):
    int_check(data['序号'][1:], True)
    dict_check(data['出租房类型'][1:], '出租房类型', True)
    miss_check(data['联系人'][1:])
    phone_check(data['联系电话'][1:], True)
    uniq_check(data['房屋编号'][1:], True)
    uniq_check(data['门牌号'][1:], True)

    for i in data['房屋编号'][1:]:
        try:
            if relation['房屋编号'].get(i['value']):
                fill('mult', i)
        except BaseException as error:
            print('error: 出租房非家庭房屋')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)
    for i in data['门牌号'][1:]:
        try:
            if relation['门牌号'].get(i['value']):
                fill('mult', i)
        except BaseException as error:
            print('error: 出租房非家庭房屋')
            print(error)
            print('data: {0}\trow: {1}\tcol: {2}'.format(i['value'], i['row'], i['col']))
            fill('error', i)

    return {
        'export': data,
        'checked': checked(data, '门牌号')
    }


def xsm(data: dict, relation: dict):
    # no relation
    int_check(data['序号'][1:], True)
    dict_check(data['与租住人关系'][1:], '与租住人关系')
    miss_check(data['姓名'][1:])
    pid_check(data['身份证号'][1:], True, True)
    dict_check(data['婚姻状况'][1:], '婚姻状况')
    dict_check(data['文化程度'][1:], '文化程度')
    phone_check(data['联系电话'][1:])
    dict_check(data['政治面貌'][1:], '政治面貌')
    date_check(data['流入日期'][1:])

    # outside relation
    relation_check_outside(data['门牌号'][1:], relation, True)

    return {
        'export': data
    }


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


def tdxx(data: dict, relation: dict):
    # no relation
    uniq_check(data['土地编号'][1:], True)
    dict_check(data['土地类别'][1:], '土地类别', True)
    int_check(data['面积（亩）'][1:], True)
    date_check(data['登记日期'][1:])
    pid_check(data['户主身份证号'][1:], True, True)

    # outside relation
    relation_check_outside(data['户主身份证号'][1:], relation, True)
    return {
        'export': data
    }


def dyxx(data: dict):
    int_check(data['序号'][1:], True)
    miss_check(data['姓名'][1:])
    pid_check(data['身份证号'][1:], True, True)
    dict_check(data['文化程度'][1:], '文化程度', True)
    phone_check(data['联系电话'][1:])
    dict_check(data['政治面貌'][1:], '党员政治面貌', True)
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


def mqrj(data: dict, relation: dict):
    # no relation
    int_check(data['序号'][1:], True)
    pid_check(data['户主身份证号'][1:], True)
    date_check(data['发生日期'][1:], True)
    miss_check(data['事件概要'][1:])
    miss_check(data['事件详情'][1:])
    dict_check(data['事件类型'][1:], '事件类型', True)
    date_check(data['完成日期'][1:])

    # outside relation
    relation_check_outside(data['户主身份证号'][1:], relation['身份证号'], True)
    relation_check_outside(data['小组'][1:], relation['小组'], True)

    return {
        'export': data
    }


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
    # 无外部关联测试
    path = {'./tests/import/1组织信息_导入模板.xlsx': zzxx,
            './tests/import/7企业信息_导入模板.xlsx': qyxx,
            './tests/import/8新型农业经营主体_导入模板.xlsx': xxnyjyzt,
            './tests/import/9厂房信息_导入模板.xlsx': cfxx,
            './tests/import/11党员信息_导入模板.xlsx': dyxx,
            './tests/import/12项目管理_导入模板.xlsx': xmgl,
            './tests/import/14租赁管理_导入模板.xlsx': zlgl}
    for k, f in path.items():
        o = Operator()
        o.import_excel(k)
        rtn = f(o.import_data)
        # print(rtn)
        o.export_data = rtn['export']
        o.export_excel(filename=('./tests/export/test' + k.split('/')[-1]))
        # print(rtn['checked'])

    # 户籍人口测试
    oz = Operator()
    oz.import_excel('./tests/import/1组织信息_导入模板.xlsx')
    rz = zzxx(oz.import_data)
    oh = Operator()
    oh.import_excel('./tests/import/2户籍人口_导入模板.xlsx')
    rh = hjrk(oh.import_data, rz['checked']['组织名称'])
    oh.export_data = rh['export']
    oh.export_excel(filename='./tests/export/test户籍人口.xlsx')

    oj = Operator()
    oj.import_excel('./tests/import/3家庭房屋_导入模板.xlsx')
    rj = jtfw(oj.import_data, rh['checked']['门牌号'])
    oj.export_data = rj['export']
    oj.export_excel(filename='./tests/export/test家庭房屋.xlsx')

    ocj = Operator()
    ocj.import_excel('./tests/import/4出租房(家庭房屋)_导入模板.xlsx')
    rcj = czfjtfw(ocj.import_data, rj['checked'])
    ocj.export_data = rcj['export']
    ocj.export_excel(filename='./tests/export/test出租房家庭房屋.xlsx')

    ocf = Operator()
    ocf.import_excel('./tests/import/5出租房(非家庭房屋)_导入模板.xlsx')
    rcf = czffjtfw(ocf.import_data, rcj['checked'])
    ocf.export_data = rcf['export']
    ocf.export_excel(filename='./tests/export/test出租房非家庭房屋.xlsx')

    ox = Operator()
    ox.import_excel('./tests/import/6新市民_导入模板.xlsx')
    t = rcj['checked']['门牌号']
    t.update(rcf['checked']['门牌号'])
    rx = xsm(ox.import_data, t)
    ox.export_data = rx['export']
    ox.export_excel(filename='./tests/export/test新市民.xlsx')

    ot = Operator()
    ot.import_excel('./tests/import/10土地信息_导入模板.xlsx')
    rt = tdxx(ot.import_data, rh['checked']['身份证号'])
    ot.export_data = rt['export']
    ot.export_excel(filename='./tests/export/test土地信息.xlsx')

    om = Operator()
    om.import_excel('./tests/import/13民情日记_导入模板.xlsx')
    r = {}
    r.update({
        '小组': rz['checked']['组织名称'],
        '身份证号': rh['checked']['身份证号']
    })
    rm = mqrj(om.import_data, r)
    om.export_data = rm['export']
    om.export_excel(filename='./tests/export/test民情日记.xlsx')
