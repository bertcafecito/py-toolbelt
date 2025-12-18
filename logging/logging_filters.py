import logging
import re


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive data in log messages."""

    # Compiled regex patterns for different sensitive data types
    PATTERNS = {
        # Credit card numbers
        "credit_card": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
        # Social Security Numbers
        "ssn": re.compile(r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"),
        # Email addresses
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
        # Phone numbers
        "phone": re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
        # IP addresses (IPv4)
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        # Passwords
        "password": re.compile(r'\b[Pp]assword\s*[:=]\s*[\'"]?([^\s\'"]{6,})[\'"]?'),
        # API keys and tokens
        "api_key": re.compile(
            r'\b[Aa][Pp][Ii][-_]?[Kk][Ee][Yy]\s*[:=]\s*[\'"]?([A-Za-z0-9_\-]{20,})[\'"]?'
        ),
        "token": re.compile(r'\b[Tt]oken\s*[:=]\s*[\'"]?([A-Za-z0-9_\-]{20,})[\'"]?'),
        # AWS credentials
        "aws_access_key": re.compile(r"\b(AKIA[0-9A-Z]{16})\b"),
        # Private keys
        "private_key": re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"
        ),
        # JWT tokens
        "jwt": re.compile(
            r"\beyJ[A-Za-z0-9_\-]*\.eyJ[A-Za-z0-9_\-]*\.[A-Za-z0-9_\-]*\b"
        ),
        # Database connection strings
        "db_connection": re.compile(
            r"\b(?:mysql|postgresql|postgres|mongodb|redis|mssql)://[^\s]+:[^\s]+@[^\s]+"
        ),
        # Generic secrets
        "secret": re.compile(r'\b[Ss]ecret\s*[:=]\s*[\'"]?([A-Za-z0-9_\-]{16,})[\'"]?'),
    }

    def filter(self, record):
        """Filter log record by masking sensitive data."""
        record.msg = self.mask_sensitive_data(record.msg)
        return True

    def mask_sensitive_data(self, message):
        """
        Mask sensitive data in the message using predefined patterns.

        Args:
            message: The log message to filter

        Returns:
            The message with sensitive data fully redacted
        """
        if not isinstance(message, str):
            message = str(message)

        # Apply each pattern to fully mask sensitive data
        for pattern_name, pattern in self.PATTERNS.items():
            message = pattern.sub(f"[REDACTED_{pattern_name.upper()}]", message)

        return message
