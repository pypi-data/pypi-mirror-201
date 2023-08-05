"""Helpers for interacting with a Slack workspace."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence, Union

from sym.sdk.exceptions.slack import SlackError  # noqa
from sym.sdk.user import User


class SlackLookupType(str, Enum):
    USER = "user"
    USER_ID = "user_id"
    USERNAME = "username"
    CHANNEL = "channel"
    GROUP = "group"
    EMAIL = "email"


@dataclass
class SlackChannel:
    lookup_type: SlackLookupType
    lookup_keys: List[Union[str, User]]
    allow_self: bool = True


def user(identifier: Union[str, User]) -> SlackChannel:
    """A reference to a Slack user.

    Users can be specified with a Slack user ID, email,
    a string version of an @mention e.g. @Jane Austen,
    or Sym :class:`~sym.sdk.user.User` instance.
    """


def mention(identifier: Union[str, User]) -> str:
    """Returns a string that mentions a Slack user given their identifier.

    Users can be specified with a Slack user ID, email,
    a string version of an @mention e.g. @Jane Austen,
    or Sym :class:`~sym.sdk.user.User` instance.
    """


def channel(name: str, allow_self: bool = False) -> SlackChannel:
    """
    A reference to a Slack channel.

    Args:
        name: The channel name to send the message to.
        allow_self: Whether to allow the current user to approve their own request.
    """


def group(users: Sequence[Union[str, User]], allow_self: bool = False) -> SlackChannel:
    """
    A reference to a Slack group.

    Args:
        users (Sequence[Union[str, User]]): A list of either Sym :class:`~sym.sdk.user.User` objects or emails.
    """


def fallback(*channels: SlackChannel) -> SlackChannel:
    """
    An instruction to try a series of `slack.channel`, `slack.user`, and `slack.group` until one succeeds.

    e.g. slack.fallback(slack.channel("#missing"), slack.user("@david"))

    Args:
        channels: any number of :class:`~sym.sdk.integrations.slack.channel`, :class:`~sym.sdk.integrations.slack.group` and :class:`~sym.sdk.integrations.slack.user`.
    """


def send_message(destination: Union[User, SlackChannel], message: str) -> None:
    """Sends a simple message to a destination in Slack. Accepts either a :class:`~sym.sdk.user.User`
    or a :class:`~sym.sdk.integrations.slack.SlackChannel`, which may represent a user, group, or channel
    in Slack.

    For example::

        # To send to #general:
        slack.send_message(slack.channel("#general"), "Hello, world!")

        # To DM a specific user:
        slack.send_message(slack.user("me@symops.io"), "It works!")

        # To DM the user who triggered an event:
        slack.send_message(event.user, "You did a thing!")

    Args:
        destination: where the message should go.
        message: the text contents of the message to send.
    """


def get_user_info(user: User) -> dict:
    """
    Get information about a Slack user.

    Refer to Slack's users.info API documentation for the details on the response format:
    https://api.slack.com/methods/users.info

    Args:
        user: The Sym user to get info about.
    """


def list_users(self, active_only: bool = True) -> list:
    """
    Returns a list of all users in the workspace.

    Refer to Slack's users.info API documentation for the details on the response format:
    https://api.slack.com/methods/users.list

    Args:
        active_only: A boolean indicating whether or not to exclude deactivated and deleted users.
    """
