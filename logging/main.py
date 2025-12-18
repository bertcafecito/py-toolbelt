import logging
import logging.config
from logging_config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def basic_logging_examples():
    """Demonstrate basic logging levels"""
    logger.debug("Debug message - for troubleshooting")
    logger.info("Application started successfully")
    logger.warning("Configuration file not found, using defaults")
    logger.error("Failed to connect to database")
    logger.critical("System is out of memory, shutting down")


def logging_with_variables():
    """Demonstrate logging with variables"""
    user, action, status = "alice", "login", "success"
    logger.info(f"User {user} performed {action} with status: {status}")
    logger.info("User action completed", extra={"user": user, "action": action, "status": status})


def logging_exceptions():
    """Demonstrate exception logging"""
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero error occurred")


def sensitive_data_examples():
    """Demonstrate sensitive data filtering in logs"""
    sensitive_data = {
        "card": "1234-5678-9012-3456",
        "ssn": "123-45-6789",
        "email": "user@example.com",
        "phone": "(555) 123-4567",
        "ip": "192.168.1.100",
        "password": "MyS3cr3tP@ssw0rd",
        "api_key": "sk_live_abc123def456ghi789jkl012mno345pqr",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
        "aws_key": "AKIAIOSFODNN7EXAMPLE",
        "db_conn": "postgresql://dbuser:dbpass123@localhost:5432/mydb"
    }
    
    for key, value in sensitive_data.items():
        logger.info(f"{key}: {value}")
    
    logger.info("User john@example.com (SSN: 987-65-4321) paid with card 4532-1234-5678-9010")


if __name__ == "__main__":
    logger.info("Starting Logging Examples")
    basic_logging_examples()
    logging_with_variables()
    logging_exceptions()
    sensitive_data_examples()
    logger.info("All Examples Completed")