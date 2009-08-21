# Copyright (C) 2009 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <http://www.gnu.org/licenses/>.

"""Information about this Mailman instance."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Info'
    ]


import sys

from zope.interface import implements

from mailman.config import config
from mailman.i18n import _
from mailman.interfaces.command import ICLISubCommand
from mailman.version import MAILMAN_VERSION_FULL



class Info:
    """Information about this Mailman instance."""

    implements(ICLISubCommand)

    name = 'info'

    def add(self, parser, command_parser):
        """See `ICLISubCommand`."""
        command_parser.add_argument(
            '-o', '--output',
            action='store', help=_("""\
            File to send the output to.  If not given, standard output is
            used."""))

    def process(self, args):
        """See `ICLISubCommand`."""

        if args.output is None:
            output = sys.stdout
        else:
            # We don't need to close output because that will happen
            # automatically when the script exits.
            output = open(args.output, 'w')

        print >> output, MAILMAN_VERSION_FULL
        print >> output, 'Python', sys.version
        print >> output, 'config file:', config.filename
        print >> output, 'db url:', config.db.url