KiwiLogger
A simple Python logger class that logs messages to Logtail, a local file, and/or the terminal. Easily configurable and customizable.

Features
Log messages to Logtail (an online logging service)
Log messages to a local file
Log messages to the terminal (stdout)
Specify the logging level (e.g., INFO, ERROR, CRITICAL)
Add structured logging (extra data) to log messages

Installation
Before using KiwiLogger, you need to install the multikiwilogger library:

bash
Copy code
pip install multikiwilogger

Usage
python

Copy code
from multikiwilogger import KiwiLogger

# Initialize the logger
mlog = KiwiLogger(log_online=True, log_local=True, log_terminal=True)

# Log a simple message
mlog('This is an INFO message.')  # Defaults to INFO level

# Log a message with a specific level
mlog('Something bad happened.', level='ERROR')

# Log a message with structured logging (extra data)
mlog('Log message with structured logging.', level='INFO', extra={
    'item': "Orange Soda",
    'price': 100.00
})

Configuration
Initialize the KiwiLogger with the following optional parameters:

name (default: __name__): The name of the logger.
level (default: logging.INFO): The minimum log level for messages.
log_online (default: True): Log messages to Logtail.
log_local (default: False): Log messages to a local file.
log_terminal (default: True): Log messages to the terminal (stdout).

Environment Variables
KiwiLogger relies on the LOGTAIL_SOURCE_TOKEN environment variable to send logs to Logtail. Set this variable in your environment or add it to a .env file:

makefile
Copy code
LOGTAIL_SOURCE_TOKEN=your_logtail_source_token_here
Replace your_logtail_source_token_here with the actual source token provided by Logtail.

License
This project is licensed under the MIT License.
