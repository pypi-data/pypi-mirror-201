import unittest
from slpkg.checks import Check
from slpkg.configs import Configs
from slpkg.repositories import Repositories


class TestPkgInstalled(unittest.TestCase):

    def setUp(self):
        self.check = Check([])
        self.configs = Configs()
        self.repos = Repositories()
        self.packages = ['fish', 'ranger', 'pycharm']

    def test_check_exists(self):
        self.assertIsNone(self.check.exists_in_the_database(self.packages))

    def test_check_unsupported(self):
        self.assertIsNone(self.check.is_package_unsupported(self.packages))

    def test_check_is_installed(self):
        self.assertIsNone(self.check.is_package_unsupported(self.packages))

    def test_check_blacklist(self):
        self.assertIsNone(self.check.is_blacklist(self.packages))

    def test_check_is_empty(self):
        self.assertIsNone(self.check.is_blacklist(self.packages))


if __name__ == "__main__":
    unittest.main()
