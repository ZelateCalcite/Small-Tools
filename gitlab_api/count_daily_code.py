import gitlab
import json
import collections


def count(
        url: str,
        token: str,
        s: str,
        e: str,
        a: str = ''
) -> dict:
    """
    Count code commit between start date and end date in gitlab

    :param url: str, gitlab url
    :param token: str, login token
    :param s: str, start date, format 'YYYY-MM-DD'
    :param e: str, end date, format 'YYYY-MM-DD'
    :param a: str, author name, default value is ''
    :return: dict, the result stored as dictionary: { "date": count }
    """
    gl = gitlab.Gitlab(url, token)
    projects = gl.projects.list(all=True)
    s = '{0}T00:00:00Z'.format(s)
    e = '{0}T00:00:00Z'.format(e)
    """
    projects:
    [
        {'id': 136, 'description': '双浜GIS大屏', 'name': 'map_gis'}
    ]
    """
    x = collections.defaultdict(lambda: {'additions': 0, 'deletions': 0, 'total': 0})
    for p in projects:
        branches = p.branches.list()
        for b in branches:
            commits = p.commits.list(all=True, query_parameters={'since': s, 'until': e, 'ref_name': b.name})
            for c in commits:
                com = p.commits.get(c.id)
                x[com.author_name]['additions'] += com.stats['additions']
                x[com.author_name]['deletions'] += com.stats['deletions']
                x[com.author_name]['total'] += com.stats['total']
    return x[a] if a in x.keys() else x


def count_daily(
        url: str,
        token: str,
        s: str,
        e: str,
        a: str = ''
) -> dict:
    """

    :param url:
    :param token:
    :param s:
    :param e:
    :param a:
    :return:
    """
    rd = {}
    sd = [int(i) for i in s[:10].split('-')]
    ed = [int(i) for i in e[:10].split('-')]
    cd = [i for i in sd]
    nd = [i for i in cd]
    # TODO: 日期转换计算程序未做
    print(sd, ed, cd, nd)
    print(cd[0] < ed[0], cd[1] < ed[1], cd[2] < ed[2])

    while cd[0] < ed[0] or cd[1] < ed[1] or cd[2] < ed[2]:
        print(cd)
        if nd[2] + 1 == 31 and nd[1] in [9]:
            nd[1] += 1
            nd[2] = 1
        elif nd[2] + 1 == 32:
            nd[1] += 1
            nd[2] = 1
        else:
            nd[2] += 1
        rd['{0}-{1}-{2}'.format(cd[0], cd[1], cd[2])] = count(url, token, s, '{0}-{1}-{2}T00:00:00Z'.format(nd[0], nd[1], nd[2]))
        cd = [i for i in nd]
    return rd


if __name__ == '__main__':
    a = count_daily('http://gitlab.jxsz.site/', 'FAUistpC9pJzvz1MXVzP', '2022-07-01T00:00:00Z', '2022-11-11T00:00:00Z')
    f = open('./count.json', 'w', encoding='utf-8')
    json.dump(a, f, ensure_ascii=False)
    f.close()
