from mock import patch

from github_util import fetch_repo_names


@patch('requests.get')
def test_fetch_repo_names(mock_get):
    mock_get.return_value.json.return_value = [
        {"name": "first"},
        {"name": "second"}]
    expected_names = ['first', 'second']

    names = fetch_repo_names('joesmith')

    assert expected_names == names
    mock_get.assert_called_once_with(
        'https://api.github.com/users/joesmith/repos')
