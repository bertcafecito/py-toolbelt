import logging
from logging_config import LOGGING
import logging.config

# Configure logging using the config from logging_config.py
logging.config.dictConfig(LOGGING)

# Get a logger instance
logger = logging.getLogger(__name__)


def basic_logging_examples():
    """Demonstrate basic logging levels and usage"""
    
    # DEBUG: Detailed information, typically for diagnosing problems
    logger.debug("This is a debug message - useful for troubleshooting")
    
    # INFO: Confirmation that things are working as expected
    logger.info("Application started successfully")
    
    # WARNING: Something unexpected happened, but the app still works
    logger.warning("Configuration file not found, using defaults")
    
    # ERROR: A serious problem, some function failed
    logger.error("Failed to connect to database")
    
    # CRITICAL: A very serious error, the program may not be able to continue
    logger.critical("System is out of memory, shutting down")


def logging_with_variables():
    """Demonstrate logging with variables and formatted strings"""
    
    user = "alice"
    action = "login"
    status = "success"
    
    # Using f-strings (Python 3.6+)
    logger.info(f"User {user} performed {action} with status: {status}")
    
    # Using extra parameter for structured logging
    logger.info(
        "User action completed",
        extra={"user": user, "action": action, "status": status}
    )
    
    # Logging numeric values
    response_time = 0.234
    status_code = 200
    logger.info(f"API request completed in {response_time}s with status {status_code}")


def logging_exceptions():
    """Demonstrate exception logging"""
    
    try:
        # Simulating an error
        result = 10 / 0
    except ZeroDivisionError as e:
        # exc_info=True includes the full stack trace
        logger.error("Division by zero error occurred", exc_info=True)
        
        # Alternative: using exception() method (automatically includes exc_info)
        logger.exception("An error occurred during calculation")


def logging_in_functions():
    """Demonstrate logging in different function contexts"""
    
    def process_data(data):
        logger.debug(f"Starting to process data: {data}")
        
        if not data:
            logger.warning("Empty data provided to process_data()")
            return None
        
        # Simulate processing
        result = len(data)
        logger.info(f"Successfully processed {result} items")
        return result
    
    # Call the function
    process_data(["item1", "item2", "item3"])
    process_data([])


def conditional_logging():
    """Demonstrate conditional logging patterns"""
    
    items_processed = 150
    threshold = 100
    
    if items_processed > threshold:
        logger.warning(
            f"Processed {items_processed} items, exceeding threshold of {threshold}"
        )
    
    # Checking log level before expensive operations
    if logger.isEnabledFor(logging.DEBUG):
        # Only compute this expensive operation if DEBUG is enabled
        expensive_debug_info = {"detail": "complex calculation result"}
        logger.debug(f"Detailed debug info: {expensive_debug_info}")


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Starting Logging Examples")
    logger.info("=" * 50)
    
    basic_logging_examples()
    print()
    
    logging_with_variables()
    print()
    
    logging_exceptions()
    print()
    
    logging_in_functions()
    print()
    
    conditional_logging()
    
    logger.info("=" * 50)
    logger.info("Logging Examples Completed")
    logger.info("=" * 50)


def sensitive_data_examples():
    """Demonstrate sensitive data filtering in logs"""
    
    logger.info("=" * 50)
    logger.info("Sensitive Data Filtering Examples")
    logger.info("=" * 50)
    
    # Credit card number
    credit_card = "1234-5678-9012-3456"
    logger.info(f"Processing payment with card: {credit_card}")
    
    # SSN
    ssn = "123-45-6789"
    logger.info(f"User SSN: {ssn}")
    
    # Email address
    email = "user@example.com"
    logger.info(f"Sending notification to: {email}")
    
    # Phone number
    phone = "(555) 123-4567"
    logger.info(f"Contact phone: {phone}")
    
    # IP address
    ip_address = "192.168.1.100"
    logger.info(f"Request from IP: {ip_address}")
    
    # Password
    password = "MyS3cr3tP@ssw0rd"
    logger.info(f"User password: {password}")
    
    # API Key
    api_key = "api_key=sk_live_abc123def456ghi789jkl012mno345pqr"
    logger.info(f"Using API key: {api_key}")
    
    # Token
    token = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
    logger.info(f"Authorization: {token}")
    
    # AWS Access Key
    aws_key = "AKIAIOSFODNN7EXAMPLE"
    logger.info(f"AWS Access Key: {aws_key}")
    
    # Database connection string
    db_conn = "postgresql://dbuser:dbpass123@localhost:5432/mydb"
    logger.info(f"Connecting to database: {db_conn}")
    
    # Secret
    secret = "secret=my_super_secret_value_12345"
    logger.info(f"Application secret: {secret}")
    
    # Private key (shortened for example)
    private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdefghijklmnopqrstuvwxyz
-----END RSA PRIVATE KEY-----"""
    logger.info(f"Using private key: {private_key}")
    
    # Mixed example - multiple sensitive data in one log
    logger.info(f"User john@example.com (SSN: 987-65-4321) paid with card 4532-1234-5678-9010")
    
    logger.info("All sensitive data should be redacted above!")
    logger.info("=" * 50)


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Starting Logging Examples")
    logger.info("=" * 50)
    
    basic_logging_examples()
    print()
    
    logging_with_variables()
    print()
    
    logging_exceptions()
    print()
    
    logging_in_functions()
    print()
    
    conditional_logging()
    print()
    
    sensitive_data_examples()
    
    logger.info("=" * 50)
    logger.info("All Examples Completed")
    logger.info("=" * 50)