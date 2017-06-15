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

'''
spark

Usage:
    spark (--help | --version)

Options:
    --help -h      display this help message and exit
    --version      print version information and exit

'''

import sys
import docopt
import spark


def main(argv=sys.argv[1:]):
    try:
        docopt.docopt(__doc__, argv=argv, version=spark.__version__)
    except docopt.DocoptExit as e:
        print(str(e), file=sys.stderr)
        return 2
    except SystemExit as e:
        return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
