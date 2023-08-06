import unittest
from slpkg.binaries.queries import BinQueries


class TestBinQueries(unittest.TestCase):

    def setUp(self):
        self.query = BinQueries('aaa_base', 'slack')

    def test_count_packages(self):
        self.assertGreater(self.query.count_packages(), 1)

    def test_all_package_names_by_repo(self):
        self.assertGreater(len(list(self.query.all_package_names_by_repo())), 1)

    def test_all_binaries_packages_by_repo(self):
        self.assertGreater(len(list(self.query.all_binaries_packages_by_repo())), 1)

    def test_all_package_names_from_repositories(self):
        self.assertGreater(len(self.query.all_package_names_from_repositories()), 1)

    def test_all_package_names_with_required(self):
        self.assertGreater(len(self.query.all_package_names_with_required()), 1)

    def test_repository(self):
        self.assertEqual('slack', self.query.repository())

    def test_package_name(self):
        self.assertEqual('aaa_base', self.query.package_name())

    def test_package_bin(self):
        self.assertEqual('aaa_base-15.0-x86_64-3.txz', self.query.package_bin())

    def test_package_checksum(self):
        self.assertEqual('ee674755e75a3f9cb3c7cfc0039f376d',
                         BinQueries('aaa_base-15.0-x86_64-3.txz', 'slack').package_checksum())

    def test_version(self):
        self.assertEqual('15.0', self.query.version())

    def test_mirror(self):
        self.assertEqual('https://slackware.uk/slackware/slackware64-15.0/', self.query.mirror())

    def test_location(self):
        self.assertEqual('slackware64/a', self.query.location())

    def test_size_comp(self):
        self.assertEqual('12 KB', self.query.size_comp())

    def test_size_uncomp(self):
        self.assertEqual('90 KB', self.query.size_uncomp())

    def test_required(self):
        self.assertEqual(['jack2', 'ladspa_sdk', 'libsbsms', 'lilv', 'lv2', 'portaudio', 'portmidi', 'portsmf', 'serd',
                          'sord', 'soundtouch', 'soxr', 'sratom', 'suil', 'twolame', 'vamp-plugin-sdk', 'wxGTK3'],
                         BinQueries('audacity', 'alien').required())

    def test_conflicts(self):
        self.assertEqual('', self.query.conflicts())

    def test_suggests(self):
        self.assertEqual('', self.query.suggests())

    def test_description(self):
        self.assertEqual('', self.query.description())


if __name__ == '__main__':
    unittest.main()
