"""
Custom exceptions for the simtwin library
"""


class CommunicationException(Exception):
    """
    General exception in client and ser communication.
    """
    def __init__(self, message):
        self.message = message


class AuthenticationException(Exception):
    """
    The authentication of the client against the server is rejected
    """
    def __init__(self, message):
        self.message = message


class ServerException(Exception):
    """
    Internal server error
    """
    def __init__(self, message):
        self.message = message


class SerializationException(Exception):
    """
    Failure to serialize object
    """
    def __init__(self, message):
        self.message = message


class DrqException(Exception):
    """
    General exception in the client side library
    """
    def __init__(self, message):
        self.message = message
