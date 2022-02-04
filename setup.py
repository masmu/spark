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

import os
import setuptools


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def load_requirements(file_path):
    if os.path.exists(file_path):
        return parse_requirements(file_path)
    else:
        return []


setuptools.setup(
    name='spark',
    version='0.0.0',
    author='Massimo Mund',
    author_email='massimo.mund@lancode.de',
    url='https://github.com/masmu/spark/',
    description='Python project pattern',
    long_description='A python3 project pattern.',
    packages=setuptools.find_packages(),
    license='GPLv3',
    platforms='Debian GNU/Linux',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=load_requirements('requirements.txt'),
    test_suite='spark.tests',
    tests_require=load_requirements('requirements-test.txt'),
    entry_points={
        'console_scripts': [
            'spark = spark.__main__:main',
        ]
    },
    data_files=[
        ('share/man/man1', ['man/spark.1']),
    ],
    package_data={
        'spark': [
        ],
    },
)
