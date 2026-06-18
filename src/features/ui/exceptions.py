"""Custom exceptions for PC Utilities Manager UI components.

This module defines specific exception types for UI-related errors to provide
better error handling and user feedback.
"""


class PCUtilitiesError(Exception):
    """Base exception for all PC Utilities Manager UI errors.

    All custom exceptions inherit from this base class to allow
    catching all UI-related errors with a single except clause.
    """

    pass


class NetworkError(PCUtilitiesError):
    """Exception raised when network operations fail.

    This includes failures to open URLs, fetch RSS feeds, or
    any other network-related operations in the UI.
    """

    def __init__(self, message: str, url: str = "", original_error: Exception | None = None):
        """Initialize network error with context.

        Args:
            message: User-friendly error message
            url: URL that failed (optional)
            original_error: The original exception that caused this error (optional)
        """
        super().__init__(message)
        self.url = url
        self.original_error = original_error

    def __str__(self) -> str:
        """Return formatted error message with URL context."""
        base_msg = super().__str__()
        if self.url:
            return f"{base_msg} (URL: {self.url})"
        return base_msg


class FeedParseError(PCUtilitiesError):
    """Exception raised when RSS feed parsing fails.

    This includes malformed XML, missing fields, or any other
    issues with parsing RSS feed data.
    """

    def __init__(self, message: str, feed_source: str = "", feed_url: str = "", original_error: Exception | None = None):
        """Initialize feed parse error with context.

        Args:
            message: User-friendly error message
            feed_source: Name of the news source (optional)
            feed_url: URL of the RSS feed that failed (optional)
            original_error: The original exception that caused this error (optional)
        """
        super().__init__(message)
        self.feed_source = feed_source
        self.feed_url = feed_url
        self.original_error = original_error

    def __str__(self) -> str:
        """Return formatted error message with feed context."""
        base_msg = super().__str__()
        if self.feed_source:
            return f"{base_msg} (Source: {self.feed_source})"
        if self.feed_url:
            return f"{base_msg} (Feed: {self.feed_url})"
        return base_msg


class DownloadHandlerError(PCUtilitiesError):
    """Exception raised when download handler operations fail.

    This includes failures to open download pages or issues with
    the download handling system.
    """

    def __init__(self, message: str, tool_name: str = "", original_error: Exception | None = None):
        """Initialize download handler error with context.

        Args:
            message: User-friendly error message
            tool_name: Name of the security tool (optional)
            original_error: The original exception that caused this error (optional)
        """
        super().__init__(message)
        self.tool_name = tool_name
        self.original_error = original_error

    def __str__(self) -> str:
        """Return formatted error message with tool context."""
        base_msg = super().__str__()
        if self.tool_name:
            return f"{base_msg} (Tool: {self.tool_name})"
        return base_msg


class ValidationError(PCUtilitiesError):
    """Exception raised when input validation fails.

    This includes invalid URLs, malformed data, or any other
    validation issues in user input.
    """

    def __init__(self, message: str, field_name: str = "", field_value: str = ""):
        """Initialize validation error with context.

        Args:
            message: User-friendly error message
            field_name: Name of the field that failed validation (optional)
            field_value: The invalid value that was provided (optional)
        """
        super().__init__(message)
        self.field_name = field_name
        self.field_value = field_value

    def __str__(self) -> str:
        """Return formatted error message with field context."""
        base_msg = super().__str__()
        if self.field_name and self.field_value:
            return f"{base_msg} (Field: {self.field_name} = '{self.field_value}')"
        if self.field_name:
            return f"{base_msg} (Field: {self.field_name})"
        return base_msg
