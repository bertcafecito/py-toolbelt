# py-toolbelt

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![AWS](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

A collection of Python utilities and tools for common development tasks.

## Features

### AWS Utilities
- **S3 Object Cleanup**: Delete S3 objects older than a specific date with support for dry-run mode and prefix filtering

### Logging
- **JSON Logging Configuration**: Pre-configured logging setup with JSON formatting
- **Sensitive Data Filtering**: Automatically filter sensitive information from logs (passwords, API keys, tokens, etc.)

## Installation

### Virtual Environment (Recommended)

We strongly recommend using a virtual environment to manage dependencies. Virtual environments:
- **Isolate project dependencies** from your system Python and other projects
- **Prevent version conflicts** between different projects requiring different package versions
- **Make your project reproducible** by keeping dependencies self-contained
- **Simplify dependency management** without affecting your global Python installation

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Install Dependencies

Once your virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Delete Old S3 Objects

Delete objects from an S3 bucket that are older than a specified date:

```bash
python aws/s3/delete_old_s3_objects.py --bucket my-bucket --date 2024-01-01
```

With prefix and dry-run mode:

```bash
python aws/s3/delete_old_s3_objects.py --bucket my-bucket --prefix folder/ --date 2024-06-15 --dry-run
```

### Logging Configuration

Use the pre-configured logging setup in your Python projects:

```python
from logging.config import dictConfig
from logging_config import LOGGING

dictConfig(LOGGING)
```

## Code Formatting with Black

This project uses [Black](https://github.com/psf/black) for code formatting. Black is an opinionated code formatter that:
- **Enforces consistent code style** across the entire project
- **Eliminates debates** about formatting preferences in code reviews
- **Saves time** by automatically formatting code instead of manual styling
- **Improves readability** with a uniform, predictable format
- **Reduces git diffs** by maintaining consistent formatting across commits

### Format Your Code

Format a single file:

```bash
black path/to/file.py
```

Format the entire project:

```bash
black .
```

Check what would be reformatted without making changes:

```bash
black --check .
```

## License

See [LICENSE](LICENSE) file for details.
