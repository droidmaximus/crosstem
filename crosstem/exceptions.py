"""
Custom exceptions for Crosstem
"""

class CrosstemError(Exception):
    """Base exception for Crosstem errors"""
    pass

class DataNotFoundError(CrosstemError):
    """Raised when required data files are not found"""
    pass

class LanguageNotSupportedError(CrosstemError):
    """Raised when requested language is not available"""
    pass
