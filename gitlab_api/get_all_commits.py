from api import base_methods

url = input('Please input git url: ')
token = input('Please input git token: ')
filename = input('Please input filename: ')

git = base_methods.get_class(url, token)
data = base_methods.get_all_commits(git)
base_methods.export_csv('./' + filename, data)
