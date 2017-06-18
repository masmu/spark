# Copyright (c) 2017 Massimo Mund <massimo.mund@lancode.de>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import unittest.mock
import pkg_resources
import gitant
import spark


distribution = pkg_resources.get_distribution('spark')
main = distribution.load_entry_point('console_scripts', 'spark')


class DistributionTest(unittest.TestCase):

    def setUp(self):
        logger_patch = unittest.mock.patch('logging.getLogger')
        self.addCleanup(logger_patch.stop)
        self.logger_mock = logger_patch.start()

    @unittest.mock.patch('builtins.print')
    def test_options(self, print_mock):
        self.assertEqual(main([]), 0)
        self.assertEqual(main(['--debug']), 0)
        self.assertEqual(main(['--help']), 0)
        self.assertEqual(main(['--invalid-argument']), 2)

    def test_get_distribution_version(self):
        self.assertEqual(
            spark.get_distribution_version(), distribution.version)

    @unittest.mock.patch('pkg_resources.get_distribution')
    def test_get_distribution_version_not_found(self, get_distribution):
        get_distribution.side_effect = pkg_resources.DistributionNotFound()
        self.assertEqual(spark.get_distribution_version(), 'unknown')

    @unittest.mock.patch('gitant.Repository')
    def test_get_git_branch_rev(self, git_repo):
        git_repo.return_value.branch = 'branch'
        git_repo.return_value.revision = 'rev'
        self.assertEqual(spark.get_git_branch_rev(), ('branch', 'rev'))

    @unittest.mock.patch.dict('sys.modules', {'gitant': None})
    def test_get_git_branch_rev_import_error(self):
        self.assertEqual(spark.get_git_branch_rev(), (None, None))

    @unittest.mock.patch('gitant.Repository')
    def test_get_git_branch_rev_invalid_repo(self, git_repo):
        git_repo.side_effect = gitant.GitDirectoryNotFoundException()
        self.assertEqual(spark.get_git_branch_rev(), (None, None))

    @unittest.mock.patch('spark._format_info_version')
    @unittest.mock.patch('spark._format_semantic_version')
    @unittest.mock.patch('spark.get_distribution_version')
    @unittest.mock.patch('spark.get_git_branch_rev')
    def test_version(
            self, get_git_branch_rev, get_distribution_version,
            _format_semantic_version, _format_info_version):
        get_distribution_version.return_value = 'version'
        get_git_branch_rev.return_value = ('branch', 'rev')
        spark.get_versions()
        _format_semantic_version.assert_called_once_with('version', 'rev')
        _format_info_version.assert_called_once_with(
            'version', 'rev', 'branch')

    @unittest.mock.patch('spark._format_info_version')
    @unittest.mock.patch('spark._format_semantic_version')
    @unittest.mock.patch('spark.get_distribution_version')
    @unittest.mock.patch.dict('os.environ', {'USE_PKG_VERSION': '1'})
    def test_version_use_pkg_version(
            self, get_distribution_version,
            _format_semantic_version, _format_info_version):
        get_distribution_version.return_value = 'version'
        spark.get_versions()
        _format_semantic_version.assert_called_once_with('version')
        _format_info_version.assert_called_once_with('version')
