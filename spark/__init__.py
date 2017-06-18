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
import pkg_resources


def get_distribution_version():
    try:
        version = pkg_resources.get_distribution(__name__).version
    except pkg_resources.DistributionNotFound:
        version = 'unknown'
    return version


def get_git_branch_rev():
    try:
        import gitant
    except Exception:
        return (None, None)
    try:
        repository = gitant.Repository(
            os.path.dirname(__file__), search_parent_directories=True)
        return (repository.branch, repository.revision)
    except (gitant.GitDirectoryNotFoundException,
            gitant.SearchParentDirectoryException):
        return (None, None)


def _format_semantic_version(version, rev=None):
    return '{version}{rev}'.format(
        version=version,
        rev='.post0.dev0+{}'.format(rev[:7]) if rev else '',
    )


def _format_info_version(version, rev=None, branch=None):
    return '{version}{rev}'.format(
        version=version,
        rev=' | git:{} ({})'.format(rev, branch) if rev else '',
    )


def get_versions():
    dist_version = get_distribution_version()
    if os.environ.get('USE_PKG_VERSION', None) == '1':
        version = _format_semantic_version(dist_version)
        version_info = _format_info_version(dist_version)
    else:
        branch, rev = get_git_branch_rev()
        version = _format_semantic_version(dist_version, rev)
        version_info = _format_info_version(dist_version, rev, branch)
    return version, version_info


__version__, __version_info__ = get_versions()
