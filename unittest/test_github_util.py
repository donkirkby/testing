from mock import patch
from unittest import TestCase

from github_util import fetch_repo_names


class GithubUtilTest(TestCase):
    @patch('requests.get')
    def test_fetch_repo_names(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"name": "first"},
            {"name": "second"}]
        expected_names = ['first', 'second']

        names = fetch_repo_names('joesmith')

        self.assertEqual(expected_names, names)
        mock_get.assert_called_once_with(
            'https://api.github.com/users/joesmith/repos')
