# Python Logging with Sensitive Data Protection

A production-ready Python logging configuration that automatically filters and redacts sensitive data from log messages. This implementation uses structured JSON logging with automatic data masking to protect PII, credentials, and other sensitive information.

## Features

- **Structured JSON Logging**: All logs are formatted as JSON for easy parsing and analysis
- **Automatic Sensitive Data Redaction**: Filters out 13+ types of sensitive data patterns
- **Dual Output**: Logs to both console (stdout) and rotating file
- **Log Rotation**: Automatic file rotation at 10MB with 5 backup files
- **Production-Ready**: Follows Python logging best practices

## Architecture

The logging system consists of three main components:

### 1. `logging_config.py` - Configuration

Defines the logging configuration using Python's `dictConfig` format:

- **Formatters**: JSON formatter using `python-json-logger`
- **Filters**: Custom `SensitiveDataFilter` applied to all handlers
- **Handlers**:
  - `stdout`: Console output with JSON formatting
  - `file`: Rotating file handler (`logs/app.log`, 10MB max, 5 backups)
- **Log Level**: DEBUG (captures all log levels)

### 2. `logging_filters.py` - Sensitive Data Filter

The `SensitiveDataFilter` class provides automatic redaction of sensitive information using regex patterns:

#### Protected Data Types

| Data Type | Pattern Example | Redacted As |
|-----------|----------------|-------------|
| Credit Cards | `1234-5678-9012-3456` | `[REDACTED_CREDIT_CARD]` |
| SSN | `123-45-6789` | `[REDACTED_SSN]` |
| Email | `user@example.com` | `[REDACTED_EMAIL]` |
| Phone Numbers | `(555) 123-4567` | `[REDACTED_PHONE]` |
| IPv4 Addresses | `192.168.1.100` | `[REDACTED_IPV4]` |
| Passwords | `password: MyP@ss123` | `[REDACTED_PASSWORD]` |
| API Keys | `api_key: sk_live_abc123...` | `[REDACTED_API_KEY]` |
| Tokens | `token: eyJhbGciOi...` | `[REDACTED_TOKEN]` |
| AWS Keys | `AKIAIOSFODNN7EXAMPLE` | `[REDACTED_AWS_ACCESS_KEY]` |
| JWT Tokens | `eyJ...` | `[REDACTED_JWT]` |
| DB Connections | `postgresql://user:pass@host/db` | `[REDACTED_DB_CONNECTION]` |
| Private Keys | `-----BEGIN PRIVATE KEY-----` | `[REDACTED_PRIVATE_KEY]` |
| Generic Secrets | `secret: abc123def456...` | `[REDACTED_SECRET]` |

#### How It Works

1. **Pre-compiled Regex**: All patterns are compiled once at class definition for performance
2. **Filter Method**: Intercepts every log record before it's written
3. **Message Masking**: Applies all patterns to the log message
4. **Arguments Masking**: Also masks any arguments passed to the logger (dict or tuple)
5. **Complete Redaction**: Replaces entire sensitive values with labeled placeholders

### 3. `main.py` - Usage Examples

Demonstrates various logging scenarios:

- **Basic Logging Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Variable Interpolation**: Logging with f-strings and extra data
- **Exception Logging**: Using `logger.exception()` for stack traces
- **Sensitive Data Examples**: Showing automatic redaction in action

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `python-json-logger==4.0.0` - JSON log formatting

## Usage

### Basic Setup

```python
import logging
import logging.config
from logging_config import LOGGING

# Configure logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

# Start logging
logger.info("Application started")
```

### Logging Examples

```python
# Basic log levels
logger.debug("Debug information")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")

# Logging with variables
user = "alice"
logger.info(f"User {user} logged in")

# Structured logging with extra fields
logger.info("User action", extra={"user": user, "action": "login", "status": "success"})

# Exception logging with stack trace
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division by zero error")
```

### Automatic Sensitive Data Protection

The filter automatically redacts sensitive data:

```python
# These will be automatically redacted
logger.info("Card: 4532-1234-5678-9010")  # → "Card: [REDACTED_CREDIT_CARD]"
logger.info("SSN: 123-45-6789")            # → "SSN: [REDACTED_SSN]"
logger.info("Email: user@example.com")     # → "Email: [REDACTED_EMAIL]"
logger.info("API Key: sk_live_abc123...")  # → "API Key: [REDACTED_API_KEY]"

# Works with complex messages too
logger.info("User john@example.com (SSN: 987-65-4321) paid with card 4532-1234-5678-9010")
# Output: "User [REDACTED_EMAIL] (SSN: [REDACTED_SSN]) paid with card [REDACTED_CREDIT_CARD]"
```

## Output Format

### JSON Log Structure

```json
{
  "asctime": "2025-12-18T12:34:56Z",
  "levelname": "INFO",
  "message": "User action completed",
  "name": "__main__",
  "funcName": "logging_with_variables",
  "lineno": 23,
  "user": "alice",
  "action": "login",
  "status": "success"
}
```

### Log Files

- **Location**: `logs/app.log`
- **Rotation**: Automatically rotates when file reaches 10MB
- **Retention**: Keeps 5 backup files (`app.log.1`, `app.log.2`, etc.)
- **Format**: JSON (one log entry per line)

## Running the Examples

```bash
cd logging
python main.py
```

This will:
1. Create the `logs/` directory if it doesn't exist
2. Run through all example scenarios
3. Output JSON logs to console and `logs/app.log`
4. Demonstrate automatic sensitive data redaction

## Security Considerations

### What This Protects

- **PII (Personally Identifiable Information)**: SSN, email, phone numbers
- **Financial Data**: Credit card numbers
- **Credentials**: Passwords, API keys, tokens, AWS keys
- **Infrastructure**: IP addresses, database connection strings
- **Cryptographic Material**: Private keys, JWT tokens

### What This Doesn't Protect

- Data stored in variables (only logs are filtered)
- Data sent to external systems before logging
- Custom sensitive patterns not in the predefined list
- Intentionally obfuscated sensitive data that doesn't match patterns

### Extending the Filter

To add custom patterns, edit `logging_filters.py`:

```python
PATTERNS = {
    # ... existing patterns ...
    'custom_pattern': re.compile(r'your-regex-here'),
}
```

## Best Practices

1. **Don't Log Raw User Input**: Always validate and sanitize user input before logging
2. **Use Structured Logging**: Prefer `extra={}` over string interpolation for searchable logs
3. **Log Levels**: Use appropriate levels (DEBUG for dev, INFO+ for production)
4. **Review Logs Regularly**: Even with filtering, periodically audit logs for leaks
5. **Complement with Other Security**: This is one layer; use encryption, access controls, etc.

## Configuration Customization

### Change Log Level

Edit `logging_config.py`:

```python
"loggers": {"": {"handlers": ["stdout", "file"], "level": "INFO"}}  # Change from DEBUG
```

### Adjust File Rotation

```python
"file": {
    "maxBytes": 20971520,  # 20MB instead of 10MB
    "backupCount": 10,      # Keep 10 backups instead of 5
}
```

### Disable Console Logging

```python
"loggers": {"": {"handlers": ["file"], "level": "DEBUG"}}  # Remove "stdout"
```

### Disable File Logging

```python
"loggers": {"": {"handlers": ["stdout"], "level": "DEBUG"}}  # Remove "file"
```

## Troubleshooting

### Logs Not Appearing

- Check log level is set appropriately
- Verify handlers are configured correctly
- Ensure `logs/` directory is writable

### Sensitive Data Still Visible

- Verify the filter is applied to all handlers
- Check if the pattern matches the data format
- Add custom regex patterns if needed

### Performance Issues

- The filter uses pre-compiled regex for efficiency
- For very high-throughput systems, consider async logging
- Test with your expected log volume

## License

See the parent directory's LICENSE file.

## Contributing

To add new sensitive data patterns:

1. Add the regex pattern to `PATTERNS` in `logging_filters.py`
2. Add test cases in `main.py`
3. Update this README with the new pattern
4. Ensure patterns are as specific as possible to avoid false positives

## Additional Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [python-json-logger](https://github.com/madzak/python-json-logger)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [Python Logging Best Practices](https://betterstack.com/community/guides/logging/python/python-logging-best-practices/#4-write-meaningful-log-messages)
