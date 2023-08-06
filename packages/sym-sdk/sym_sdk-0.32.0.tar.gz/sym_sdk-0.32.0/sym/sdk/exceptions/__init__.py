"""Exceptions that can be raised by the Sym Runtime."""

__all__ = [
    "AccessStrategyError",
    "AptibleError",
    "AWSError",
    "AWSLambdaError",
    "CouldNotSaveError",
    "ExceptionWithHint",
    "GitHubError",
    "HTTPError",
    "IdentityError",
    "MissingArgument",
    "OktaError",
    "OneLoginError",
    "PagerDutyError",
    "SDKError",
    "SlackError",
    "SymException",
]

from .access_strategy import AccessStrategyError
from .aptible import AptibleError
from .aws import AWSError, AWSLambdaError
from .github import GitHubError
from .http import HTTPError
from .identity import CouldNotSaveError, IdentityError
from .okta import OktaError
from .onelogin import OneLoginError
from .pagerduty import PagerDutyError
from .sdk import MissingArgument, SDKError
from .slack import SlackError
from .sym_exception import ExceptionWithHint, SymException
