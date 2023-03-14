import gitlab
import collections
import json

url = 'http://gitlab.jxsz.site/'
# token = 'NYwDpycRLpKiJs7SKTyg'  # 后端
token = 'FAUistpC9pJzvz1MXVzP'  # 前端
gl = gitlab.Gitlab(url, token)
start = '2022-07-01T00:00:00Z'
end = '2022-10-01T00:00:00Z'
projects = gl.projects.list(all=True)
"""
projects:
[
    {'id': 136, 'description': '双浜GIS大屏', 'name': 'map_gis'}
]
"""
a = {}
x = collections.defaultdict(lambda: {'additions': 0, 'deletions': 0, 'total': 0})
for p in projects:
    branches = p.branches.list()
    d = collections.defaultdict(lambda: {'additions': 0, 'deletions': 0, 'total': 0})
    for b in branches:
        commits = p.commits.list(all=True, query_parameters={'since': start, 'until': end, 'ref_name': b.name})
        for c in commits:
            com = p.commits.get(c.id)
            d[com.author_name]['additions'] += com.stats['additions']
            d[com.author_name]['deletions'] += com.stats['deletions']
            d[com.author_name]['total'] += com.stats['total']
            x[com.author_name]['additions'] += com.stats['additions']
            x[com.author_name]['deletions'] += com.stats['deletions']
            x[com.author_name]['total'] += com.stats['total']
    a[p.description] = d

f = open('./count.json', 'w', encoding='utf-8')
json.dump(a, f, ensure_ascii=False)
f.close()
f = open('./count1.json', 'w', encoding='utf-8')
json.dump(x, f, ensure_ascii=False)
f.close()
