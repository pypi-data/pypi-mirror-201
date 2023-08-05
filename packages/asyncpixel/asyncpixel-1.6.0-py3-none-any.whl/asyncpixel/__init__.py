"""Asyncpixel.

An asyncronous hypixel api wrapper
"""
#  Copyright (C) 2020 Leon Bowie
# This program is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License a
# long with this program. If not, see <https://www.gnu.org/licenses/>.
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from . import utils
from .hypixel import Hypixel

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
__author__ = "Leon Bowie"
__copyright__ = "Copyright 2020-2023 Leon Bowie"
__title__ = "asyncpixel"
__license__ = """Copyright (C) 2020 Leon Bowie

This program is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License a
long with this program. If not, see <https://www.gnu.org/licenses/>."""

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Hypixel",
    "utils",
]
