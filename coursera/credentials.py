# -*- coding: utf-8 -*-

"""
Manages the credential information (passwords, etc).
"""

import getpass
import logging
import os
import platform

try:
    import keyring
except ImportError:
    keyring = None

KEYRING_SERVICE_NAME = 'coursera-dl'


class CredentialsError(BaseException):
    """
    Class to be thrown if the credentials are not found.
    """

    pass


def _getenv_or_empty(s):
    """
    Helper function that converts None gotten from the environment to the
    empty string.
    """
    return os.getenv(s) or ""

def get_credentials(username=None, password=None, use_keyring=False):
    """
    Return valid username, password tuple.

    Raises CredentialsError if username or password is missing.
    """

    if not username:
        raise CredentialsError(
            'Please provide a username with the -u option, '
            'or a CAUTH cookie with the --cauth option')

    if not password and use_keyring:
        password = keyring.get_password(KEYRING_SERVICE_NAME, username)

    if not password:
        password = getpass.getpass('Coursera password for {0}: '.format(username))
        if use_keyring:
            keyring.set_password(KEYRING_SERVICE_NAME, username, password)

    return username, password
