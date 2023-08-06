import unittest

from slpkg.utilities import Utilities
from slpkg.upgrade import Upgrade


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.utils = Utilities()
        self.packages: list = ['wget', 'vim', 'pycharm', 'libreoffice', 'ptpython', 'ranger', 'colored']

    def test_installed_is_upgradable_for_binaries(self):
        for pkg in self.packages:
            self.assertFalse(False, Upgrade(['-B', '--bin-repo='], 'slack_patches').is_package_upgradeable(pkg))

    def test_installed_is_upgradable_for_slackbuilds(self):
        for pkg in self.packages:
            self.assertFalse(False, Upgrade([]).is_package_upgradeable(pkg))

    def test_for_sbo_repository(self):
        upgrade = Upgrade([])
        packages: list = list(upgrade.packages())
        self.assertGreater(len(packages), 1)

    def test_for_alien_repository(self):
        upgrade = Upgrade(['-B'], 'alien')
        packages: list = list(upgrade.packages())
        self.assertGreater(len(packages), 1)

    def test_for_slack_repository(self):
        upgrade = Upgrade(['-B'], 'slack')
        packages: list = list(upgrade.packages())
        self.assertGreater(len(packages), 1)


if __name__ == '__main__':
    unittest.main()
