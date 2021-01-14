# Copyright (C) 2010-2021 by the Free Software Foundation, Inc.
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
# GNU Mailman.  If not, see <https://www.gnu.org/licenses/>.

"""Interface to bounce detection components."""

from enum import Enum
from public import public
from zope.interface import Attribute, Interface


class InvalidBounceEvent(Exception):
    """An invalid bounce event was found during processing.

    This either means the email is no longer a member or the MailingList does
    not exist anymore.
    """


@public
class BounceContext(Enum):
    """The context in which the bounce was detected."""

    # This is a normal bounce detection.  IOW, Mailman received a bounce in
    # response to a mailing list post.
    normal = 1

    # A probe email bounced.  This can be considered a bit more serious, since
    # it occurred in response to a specific message to a specific user.
    probe = 2


@public
class UnrecognizedBounceDisposition(Enum):
    # Just throw the message away.
    discard = 0
    # Forward the message to the list administrators, which includes both the
    # owners and the moderators.
    administrators = 1
    # Forward the message to the site owner.
    site_owner = 2


@public
class IBounceEvent(Interface):
    """Registration record for a single bounce event."""

    list_id = Attribute(
        """The List-ID of the mailing list that received this bounce.""")

    email = Attribute(
        """The email address that bounced.""")

    timestamp = Attribute(
        """The timestamp for when the bounce was received.""")

    message_id = Attribute(
        """The Message-ID of the bounce message.""")

    context = Attribute(
        """Where was the bounce detected?""")

    processed = Attribute(
        """Has this bounce event been processed?""")


@public
class IBounceProcessor(Interface):
    """Manager/processor of bounce events."""

    def register(mlist, email, msg, context=None):
        """Register a bounce event.

        :param mlist: The mailing list that the bounce occurred on.
        :type mlist: IMailingList
        :param email: The email address that is bouncing.
        :type email: str
        :param msg: The bounce message.
        :type msg: email.message.Message
        :param context: In what context was the bounce detected?  The default
            is 'normal' context (i.e. we received a normal bounce for the
            address).
        :type context: BounceContext
        :return: The registered bounce event.
        :rtype: IBounceEvent
        """

    def process_event(event):
        """Process a single bounce event.

        :param event: The bounce event to process.
        :type event: IBounceEvent
        """

    def send_warnings_and_remove():
        """Send warnings to disabled users and remove them if needed.

        All users, that have their delivery disabled, get warnings about being
        un-subscribed until Mailinglist's maximum configured numbered of
        warnings are sent and then remove the user.
        """

    events = Attribute(
        """An iterator over all events.""")

    unprocessed = Attribute(
        """An iterator over all unprocessed bounce events.""")
