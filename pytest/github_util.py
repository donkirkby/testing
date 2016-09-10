import requests


def fetch_repo_names(username):
    url = ('https://api.github.com/users/{}'
           '/repos'.format(username))
    repos = requests.get(url).json()
    return [repo['name'] for repo in repos]
