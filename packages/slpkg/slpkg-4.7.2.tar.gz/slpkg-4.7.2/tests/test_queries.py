import unittest
from slpkg.sbos.queries import SBoQueries


class TestSBoQueries(unittest.TestCase):

    def setUp(self):
        self.query = SBoQueries('slpkg')

    def test_slackbuild(self):
        self.assertEqual('slpkg', self.query.slackbuild())

    def test_location(self):
        self.assertEqual('system', self.query.location())

    def test_sources(self):
        self.assertEqual(['https://gitlab.com/dslackw/slpkg/-/archive'
                         '/4.5.3/slpkg-4.5.3.tar.gz'], self.query.sources())

    def test_requires(self):
        self.assertEqual(['SQLAlchemy', 'python3-pythondialog', 'python3-progress'], self.query.requires())

    def test_version(self):
        self.assertEqual('4.5.3', self.query.version())

    def test_checksum(self):
        self.assertListEqual(['d76c95208a4c1cc2d6121417885eb8a8'],
                             self.query.checksum())

    def test_files(self):
        self.assertEqual(5, len(self.query.files().split()))

    def test_description(self):
        self.assertEqual('slpkg (Slackware Packaging Tool)',
                         self.query.description())

    def test_names(self):
        self.assertIn('slpkg', self.query.sbos())


if __name__ == '__main__':
    unittest.main()
