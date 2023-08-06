import unittest

from slpkg.utilities import Utilities
from slpkg.upgrade import Upgrade


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.utils = Utilities()
        self.packages: list = ['git', 'wget', 'vim', 'pycharm', 'libreoffice', 'ptpython', 'ranger', 'colored']

    def test_installed_is_upgradable_for_binaries(self):
        for pkg in self.packages:
            self.assertFalse(False, Upgrade(['-B', '--bin-repo='], 'slack_patches').is_package_upgradeable(pkg))

    def test_installed_is_upgradable_for_slackbuilds(self):
        for pkg in self.packages:
            self.assertFalse(False, Upgrade([]).is_package_upgradeable(pkg))


if __name__ == '__main__':
    unittest.main()
