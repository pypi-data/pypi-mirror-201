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
                         '/4.6.1/slpkg-4.6.1.tar.gz'], self.query.sources())

    def test_requires(self):
        self.assertEqual(['SQLAlchemy', 'python3-pythondialog', 'python3-progress'], self.query.requires())

    def test_version(self):
        self.assertEqual('4.6.1', self.query.version())

    def test_checksum(self):
        self.assertListEqual(['8f98a8f666f8772be205ce65214dd538'],
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
