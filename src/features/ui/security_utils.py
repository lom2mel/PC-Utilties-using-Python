"""Security utilities for URL validation and safe browser operations.

This module provides security-critical functions for validating URLs and
safely opening them in browsers, preventing XSS attacks and open redirect
vulnerabilities.
"""

import logging
import webbrowser
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Security constants
ALLOWED_PROTOCOLS = {'http', 'https'}
MAX_URL_LENGTH = 2048
DANGEROUS_PROTOCOLS = {'javascript:', 'data:', 'file:', 'ftp:', 'mailto:', 'irc:'}


def validate_url(url: str) -> bool:
    """Validate URL for security and safety.

    This function performs comprehensive URL validation to prevent
    XSS attacks, open redirect vulnerabilities, and dangerous protocol
    execution.

    Args:
        url: URL to validate

    Returns:
        True if URL is safe to open, False otherwise

    Security checks:
        - Rejects empty or non-string URLs
        - Only allows http:// and https:// protocols
        - Blocks protocol-relative URLs (//evil.com)
        - Enforces reasonable URL length limits
        - Validates URL structure using urllib.parse
    """
    # Basic type and content validation
    if not url or not isinstance(url, str):
        logger.warning(f"URL validation failed: Invalid input type or empty URL")
        return False

    # Check URL length limits
    if len(url) > MAX_URL_LENGTH:
        logger.warning(f"URL validation failed: URL too long ({len(url)} > {MAX_URL_LENGTH})")
        return False

    # Check for dangerous protocols
    url_lower = url.lower()
    for protocol in DANGEROUS_PROTOCOLS:
        if url_lower.startswith(protocol):
            logger.warning(f"URL validation failed: Dangerous protocol '{protocol}' detected")
            return False

    # Block protocol-relative URLs
    if url.startswith('//'):
        logger.warning("URL validation failed: Protocol-relative URL detected")
        return False

    try:
        # Parse and validate URL structure
        parsed = urlparse(url)

        # Only allow http and https protocols
        if parsed.scheme not in ALLOWED_PROTOCOLS:
            logger.warning(f"URL validation failed: Invalid protocol '{parsed.scheme}'")
            return False

        # Ensure we have a valid network location
        if not parsed.netloc:
            logger.warning("URL validation failed: No network location in URL")
            return False

        # Additional safety checks
        # Block localhost and local network access if needed
        # (can be enhanced based on security requirements)

        return True

    except Exception as e:
        logger.warning(f"URL validation failed: Parsing error - {str(e)[:100]}")
        return False


def validate_and_open_url(url: str) -> bool:
    """Validate and safely open URL in default web browser.

    This function combines URL validation with safe browser opening,
    providing a secure interface for external URL access.

    Args:
        url: URL to validate and open

    Returns:
        True if URL was successfully opened, False otherwise

    Security features:
        - Full URL validation before opening
        - Comprehensive logging of all operations
        - Exception handling for browser failures
        - Safe fallback for validation failures
    """
    # Validate URL first
    if not validate_url(url):
        logger.warning(f"Rejected unsafe URL: {url[:100]}...")
        return False

    try:
        # Open URL in default browser
        webbrowser.open(url)
        logger.info(f"Successfully opened safe URL: {url[:100]}...")
        return True

    except Exception as e:
        logger.error(f"Failed to open URL: {str(e)[:100]}")
        return False


def sanitize_url_for_logging(url: str, max_length: int = 50) -> str:
    """Sanitize URL for safe logging (truncate if needed).

    Args:
        url: URL to sanitize
        max_length: Maximum length for logged URL

    Returns:
        Sanitized URL safe for logging
    """
    if not url:
        return ""

    # Truncate URL if too long
    if len(url) > max_length:
        return url[:max_length] + "..."

    return url
