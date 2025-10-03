"""
HTTP Client module for making API requests.

This package provides base classes and implementations for making HTTP requests
to external APIs in a consistent, reliable manner.
"""

from imp_bot.utils.clients.base_client import BaseHttpClient, ClientError
from imp_bot.utils.clients.bartender_client import BartenderClient, BartenderClientError

__all__ = [
    'BaseHttpClient',
    'ClientError',
    'BartenderClient',
    'BartenderClientError',
]