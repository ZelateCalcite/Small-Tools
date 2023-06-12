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
            if not i['value'].isdigit():
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
                if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
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
        if wrong.get(i['row']) == 0:
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


def zzxx(data: dict) -> dict:
    # result = {
    #     'checked': defaultdict(int),
    # }
    # wrong = defaultdict(int)

    int_check(data['序号'][1:], True)
    # for zindex in data['序号'][1:]:
    #     try:
    #         if zindex['value'] is None:
    #             fill('miss', zindex)
    #             wrong[zindex['row']] += 1
    #             continue
    #         if not zindex['value'].isdigit():
    #             fill('type', zindex)
    #             wrong[zindex['row']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', zindex)

    miss_check(data['组织名称'][1:])
    # for zname in data['组织名称'][1:]:
    #     try:
    #         if ['value'] is None:
    #             fill('miss', zname)
    #             wrong[zname['row']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', zname)

    dict_check(data['组织类型'][1:], '组织类型', True)
    # for ztype in data['组织类型'][1:]:
    #     try:
    #         if ztype['value'] is None:
    #             fill('miss', ztype)
    #             wrong[ztype['row']] += 1
    #             continue
    #         if not check.dict_check('组织类型', ztype['value']):
    #             fill('dict', ztype)
    #             wrong[ztype['row']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', ztype)

    int_check(data['排序序号'][1:])
    # for zsort in data['排序序号'][1:]:
    #     try:
    #         if zsort['value'] is not None and not zsort['value'].isdigit():
    #             fill('type', zsort)
    #             wrong[zsort['row']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', zsort)

    phone_check(data['联系电话'][1:])
    # for zphone in data['联系电话'][1:]:
    #     try:
    #         if zphone['value'] is not None:
    #             stat = check.phone_check(zphone['value'])
    #             if stat == 'wrong length':
    #                 fill('leng', zphone)
    #                 wrong[zphone['row']] += 1
    #             elif stat == 'wrong character':
    #                 fill('type', zphone)
    #                 wrong[zphone['row']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', zphone)

    # for zname in data['组织名称'][1:]:
    #     if wrong.get(zname['row']) == 0:
    #         result['checked'].update({zname['value']: 1})

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
    # for qindex in data['序号'][1:]:
    #     try:
    #         if qindex['value'] is None:
    #             fill('miss', qindex)
    #             continue
    #         if not qindex['value'].isdigit():
    #             fill('type', qindex)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qindex)

    uniq_check(data['企业名称'][1:], True)
    # name = defaultdict(int)
    # for qname in data['企业名称'][1:]:
    #     try:
    #         if qname['value'] is None:
    #             fill('miss', qname)
    #             continue
    #         name[qname['value']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qname)
    # for qname in data['企业名称'][1:]:
    #     try:
    #         if not check.uniq_check(name, qname['value']):
    #             fill('uniq', qname)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qname)

    uniq_check(data['统一社会信用代码'][1:])
    # code = defaultdict(int)
    # for qcode in data['统一社会信用代码'][1:]:
    #     try:
    #         if ['value'] is not None:
    #             code[qcode['value']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qcode)
    # for qcode in data['统一社会信用代码'][1:]:
    #     try:
    #         if not check.uniq_check(code, qcode['value']):
    #             fill('uniq', qcode)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qcode)

    uniq_check(data['门牌号'][1:], True)
    # address = defaultdict(int)
    # for qaddress in data['门牌号'][1:]:
    #     try:
    #         if qaddress['value'] is None:
    #             fill('miss', qaddress)
    #             continue
    #         address[qaddress['value']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qaddress)
    # for qaddress in data['门牌号'][1:]:
    #     try:
    #         if not check.uniq_check(address, qaddress['value']):
    #             fill('uniq', qaddress)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qaddress)

    dict_check(data['企业类型'][1:], '企业类型', True)
    # for qtype in data['企业类型'][1:]:
    #     try:
    #         if qtype['value'] is None:
    #             fill('miss', qtype)
    #             continue
    #         if not check.dict_check('企业类型', qtype['value']):
    #             fill('dict', qtype)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qtype)

    dict_check(data['企业状态'][1:], '企业状态', True)
    # for qstatus in data['企业状态'][1:]:
    #     try:
    #         if qstatus['value'] is None:
    #             fill('miss', qstatus)
    #             continue
    #         if not check.dict_check('企业状态', qstatus['value']):
    #             fill('dict', qstatus)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qstatus)

    miss_check(data['法人代表'][1:])
    # for LR in data['法人代表'][1:]:
    #     try:
    #         if LR['value'] is None:
    #             fill('miss', LR)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', LR)

    date_check(data['成立日期'][1:], True)
    # for SD in data['成立日期'][1:]:
    #     try:
    #         if SD['value'] is None:
    #             fill('miss', SD)
    #             continue
    #         temp = SD['value'].split('/')
    #         if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
    #             if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
    #                 stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
    #                 if stat == 'checked':
    #                     SD['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
    #                     continue
    #         fill('date', SD)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', SD)

    int_check(data['注册资本（万）'][1:], True)
    # for RC in data['注册资本（万）'][1:]:
    #     try:
    #         if RC['value'] is None:
    #             fill('miss', RC)
    #             continue
    #         if not RC['value'].isdigit():
    #             fill('type', RC)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', RC)

    miss_check(data['注册地址'][1:])
    # for RA in data['注册地址'][1:]:
    #     try:
    #         if RA['value'] is None:
    #             fill('miss', RA)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', RA)

    date_check(data['入驻日期'][1:], True)
    # for ED in data['入驻日期'][1:]:
    #     try:
    #         if ED['value'] is None:
    #             fill('miss', ED)
    #             continue
    #         temp = ED['value'].split('/')
    #         if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
    #             if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
    #                 stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
    #                 if stat == 'checked':
    #                     ED['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
    #                     continue
    #         fill('date', ED)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', ED)

    date_check(data['迁出日期'][1:])
    # for LD in data['迁出日期'][1:]:
    #     try:
    #         if LD['value'] is None:
    #             continue
    #         temp = LD['value'].split('/')
    #         if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
    #             if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
    #                 stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
    #                 if stat == 'checked':
    #                     LD['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
    #                     continue
    #         fill('date', LD)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', LD)

    dict_check(data['所属行业'][1:], '所属行业')
    # for qindustry in data['所属行业'][1:]:
    #     try:
    #         if qindustry['value'] is None:
    #             continue
    #         if not check.dict_check('所属行业', qindustry['value']):
    #             fill('dict', qindustry)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', qindustry)

    int_check(data['实缴资本（万）'][1:])
    # for PC in data['实缴资本（万）'][1:]:
    #     try:
    #         if PC['value'] is None:
    #             continue
    #         if not PC['value'].isdigit():
    #             fill('type', PC)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', PC)

    date_check(data['核准日期'][1:])
    # for AD in data['核准日期'][1:]:
    #     try:
    #         if AD['value'] is None:
    #             continue
    #         temp = AD['value'].split('/')
    #         if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
    #             if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
    #                 stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
    #                 if stat == 'checked':
    #                     AD['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
    #                     continue
    #         fill('date', AD)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', AD)

    dict_check(data['纳税人资质'][1:], '纳税人资质')
    # for TQ in data['纳税人资质'][1:]:
    #     try:
    #         if TQ['value'] is None:
    #             continue
    #         if not check.dict_check('纳税人资质', TQ['value']):
    #             fill('dict', TQ)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', TQ)

    phone_check(data['联系电话'][1:])
    # for phone in data['联系电话'][1:]:
    #     try:
    #         if phone['value'] is not None:
    #             stat = check.phone_check(phone['value'])
    #             if stat == 'wrong length':
    #                 fill('leng', phone)
    #             elif stat == 'wrong character':
    #                 fill('type', phone)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', phone)

    int_check(data['占地面积（亩）'][1:], True)
    # for OA in data['占地面积（亩）'][1:]:
    #     try:
    #         if OA['value'] is None:
    #             fill('miss', OA)
    #             continue
    #         if not OA['value'].isdigit():
    #             fill('type', OA)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', OA)

    return {
        'export': data
    }


def xxnyjyzt(data: dict) -> dict:
    int_check(data['序号'][1:], True)
    # for nindex in data['序号'][1:]:
    #     try:
    #         if nindex['value'] is None:
    #             fill('miss', nindex)
    #             continue
    #         if not nindex['value'].isdigit():
    #             fill('type', nindex)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', nindex)

    miss_check(data['主体名称'][1:])
    # for PN in data['主体名称'][1:]:
    #     try:
    #         if PN['value'] is None:
    #             fill('miss', PN)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', PN)

    dict_check(data['主体类型'][1:], '主体类型', True)
    # for PT in data['主体类型'][1:]:
    #     try:
    #         if PT['value'] is None:
    #             fill('miss', PT)
    #             continue
    #         if not check.dict_check('主体类型', PT['value']):
    #             fill('dict', PT)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', PT)

    miss_check(data['产业'][1:])
    # for nindustry in data['产业'][1:]:
    #     try:
    #         if nindustry['value'] is None:
    #             fill('miss', nindustry)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', nindustry)

    miss_check(data['法人'][1:])
    # for LP in data['法人'][1:]:
    #     try:
    #         if LP['value'] is None:
    #             fill('miss', LP)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', LP)

    phone_check(data['联系电话'][1:])
    # for phone in data['联系电话'][1:]:
    #     try:
    #         if phone['value'] is not None:
    #             stat = check.phone_check(phone['value'])
    #             if stat == 'wrong length':
    #                 fill('leng', phone)
    #             elif stat == 'wrong character':
    #                 fill('type', phone)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', phone)

    return {
        'export': data
    }


def cfxx(data: dict) -> dict:
    int_check(data['序号'][1:], True)
    # for cindex in data['序号'][1:]:
    #     try:
    #         if cindex['value'] is None:
    #             fill('miss', cindex)
    #             continue
    #         if not cindex['value'].isdigit():
    #             fill('type', cindex)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', cindex)

    uniq_check(data['厂房名称'][1:], True)
    # name = defaultdict(int)
    # for cname in data['厂房名称'][1:]:
    #     try:
    #         if cname['value'] is None:
    #             fill('miss', cname)
    #             continue
    #         name[cname['value']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', cname)
    # for cname in data['厂房名称'][1:]:
    #     try:
    #         if not check.uniq_check(name, cname['value']):
    #             fill('uniq', cname)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', cname)

    int_check(data['建筑面积(m²)'][1:], True)
    # for area in data['建筑面积(m²)'][1:]:
    #     try:
    #         if area['value'] is None:
    #             fill('miss', area)
    #             continue
    #         if not area['value'].isdigit():
    #             fill('type', area)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', area)

    date_check(data['建造日期'][1:], True)
    # for CD in data['建造日期'][1:]:
    #     try:
    #         if CD['value'] is None:
    #             fill('miss', CD)
    #             continue
    #         temp = CD['value'].split('/')
    #         if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
    #             if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
    #                 stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
    #                 if stat == 'checked':
    #                     CD['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
    #                     continue
    #         fill('date', CD)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', CD)

    date_check(data['拆除日期'][1:])
    # for DD in data['拆除日期'][1:]:
    #     try:
    #         if DD['value'] is None:
    #             continue
    #         temp = DD['value'].split('/')
    #         if len(temp) == 3 and len(temp[0]) == 4 and len(temp[1]) <= 2 and len(temp[2]) <= 2:
    #             if temp[0].isdigit() and temp[1].isdigit() and temp[2].isdigit():
    #                 stat = check.date_check(temp[0] + temp[1].zfill(2) + temp[2].zfill(2))
    #                 if stat == 'checked':
    #                     DD['value'] = '{0}/{1}/{2}'.format(temp[0], temp[1].zfill(2), temp[2].zfill(2))
    #                     continue
    #         fill('date', DD)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', DD)

    miss_check(data['联系人'][1:])
    # for contact in data['联系人'][1:]:
    #     try:
    #         if contact['value'] is None:
    #             fill('miss', contact)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', contact)

    phone_check(data['联系电话'][1:])
    # for phone in data['联系电话'][1:]:
    #     try:
    #         if phone['value'] is not None:
    #             stat = check.phone_check(phone['value'])
    #             if stat == 'wrong length':
    #                 fill('leng', phone)
    #             elif stat == 'wrong character':
    #                 fill('type', phone)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', phone)

    return {
        'export': data
    }


def tdxx():
    pass


def dyxx(data: dict):
    int_check(data['序号'][1:], True)
    # for dindex in data['序号'][1:]:
    #     try:
    #         if dindex['value'] is None:
    #             fill('miss', dindex)
    #             continue
    #         if not dindex['value'].isdigit():
    #             fill('type', dindex)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', dindex)

    miss_check(data['姓名'][1:])
    # for dname in data['姓名'][1:]:
    #     try:
    #         if dname['value'] is None:
    #             fill('miss', dname)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', dname)

    pid_check(data['身份证号'][1:], True, True)
    # pid = defaultdict(int)
    # for dpid in data['身份证号'][1:]:
    #     try:
    #         if dpid['value'] is None:
    #             fill('miss', dpid)
    #             continue
    #         temp = check.pid_check(dpid['value'])
    #         if temp == 'wrong character':
    #             fill('type', dpid)
    #         elif temp == 'wrong length':
    #             fill('leng', dpid)
    #         elif temp != 'checked':
    #             fill('date', dpid)
    #         else:
    #             pid[dpid['value']] += 1
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', dpid)
    # for dpid in data['身份证号'][1:]:
    #     try:
    #         if not check.uniq_check(pid, dpid['value']):
    #             fill('uniq', dpid)
    #     except BaseException as error:
    #         print('error:')
    #         print(error)
    #         fill('error', dpid)

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

    # operator.import_excel('./tests/import/1组织信息_导入模板.xlsx')
    # operator.import_excel('./tests/import/7企业信息_导入模板.xlsx')
    # operator.import_excel('./tests/import/8新型农业经营主体_导入模板.xlsx')
    # operator.import_excel('./tests/import/9厂房信息_导入模板.xlsx')
    operator.import_excel('./tests/import/11党员信息_导入模板.xlsx')

    # rtn = zzxx(operator.import_data)
    # rtn = qyxx(operator.import_data)
    # rtn = xxnyjyzt(operator.import_data)
    # rtn = cfxx(operator.import_data)
    rtn = dyxx(operator.import_data)

    operator.export_data = rtn['export']

    # operator.export_excel(filename='./tests/export/test组织信息_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test企业信息_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test新型农业经营主体_导入模板.xlsx')
    # operator.export_excel(filename='./tests/export/test厂房信息_导入模板.xlsx')
    operator.export_excel(filename='./tests/export/test党员信息_导入模板.xlsx')

    # print(rtn['checked'])
