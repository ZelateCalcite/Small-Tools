import gitlab
import pandas as pd


def get_class(url: str, token: str) -> gitlab.Gitlab:
    return gitlab.Gitlab(url, private_token=token)


def get_all_commits(gitlab_class: gitlab.Gitlab, start_date='', end_date='') -> [dict]:
    projects = gitlab_class.projects.list(all=True)  # list of all projects belong to the git
    data = []  # return data
    for project in projects:
        for branch in project.branches.list():  # project.branches: list of all branched belong to the project
            param = {'ref_name': branch.name}
            if start_date and end_date:
                param.update({'since': start_date, 'until': end_date})
            commits = project.commits.list(all=True, query_parameters=param)  # list of all commits belong to the branch
            for commit in commits:
                com = project.commits.get(commit.id)  # get all commit info by id
                print('{0}\t{1}\t{2}'.format(project.path_with_namespace, branch.name, com.committed_date))
                pro = {}
                try:
                    pro['project name'] = project.path_with_namespace
                    pro['author name'] = com.author_name
                    pro['branch'] = branch.name
                    pro['date'] = com.committed_date
                    pro['additions'] = com.stats['additions']
                    pro['deletions'] = com.stats['deletions']
                    pro['commitNum'] = com.stats['total']
                    data.append(pro)
                finally:  # avoid network error
                    pass
    print('Successfully Finished')
    return data


def export_csv(file_name: str, export_data: [dict]) -> None:
    column = ['project name', 'author name', 'branch', 'date', 'additions', 'deletions', 'commitNum']
    dataframe = pd.DataFrame(export_data, columns=column)
    dataframe.to_csv(file_name, index=False, encoding='utf_8_sig')


if __name__ == '__main__':
    url = 'http://gitlab.jxsz.site/'
    token = 'FAUistpC9pJzvz1MXVzP'
    gl_d = gitlab.Gitlab(url, private_token=token)

    start_d = '2022-07-01T00:00:00Z'
    end_d = '2023-03-17T00:00:00Z'
    l = get_all_commits(gl_d, start_date=start_d, end_date=end_d)
    export_csv('./all.csv', l)
