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
import spark


distribution = pkg_resources.get_distribution("spark")
main = distribution.load_entry_point("console_scripts", "spark")


class DistributionTest(unittest.TestCase):

    @unittest.mock.patch("builtins.print")
    def test_options(self, print):
        self.assertEqual(main(["--invalid-argument"]), 2)
        self.assertEqual(main(["--help"]), 0)

    def test_version(self):
        self.assertEqual(spark.__version__, distribution.version)
        self.assertRegex(spark.__version__, r'\d+\.\d+\.\d+')
