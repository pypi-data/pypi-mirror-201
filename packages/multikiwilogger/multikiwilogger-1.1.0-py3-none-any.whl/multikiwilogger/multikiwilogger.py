import os
import sys
import logging
from logtail import LogtailHandler
from datetime import datetime
import inspect

def get_terminal_logger(name):
    """Creates a logger that outputs logs to the terminal."""
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def get_online_logger(name):
    """Creates a logger that sends logs to Logtail."""
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(message)s')
    logtail_source_token = os.environ.get("LOGTAIL_SOURCE_TOKEN")
    if logtail_source_token:
        try:
            handler = LogtailHandler(source_token=logtail_source_token)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        except ConnectionError as e:
            # If Logtail server is unreachable, raise an exception
            raise ConnectionError(f"Error connecting to Logtail: {e}")
    else:
        # If LOGTAIL_SOURCE_TOKEN environment variable is not set, raise an exception
        raise ValueError("Error: LOGTAIL_SOURCE_TOKEN environment variable not found.")
    logger.setLevel(logging.DEBUG)
    return logger

def get_file_logger(name, filename):
    """Creates a logger that writes logs to a file."""
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    try:
        handler = logging.FileHandler(filename)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except FileNotFoundError as e:
        # If log file path is invalid, raise an exception
        raise FileNotFoundError(f"Error creating file logger: {e}")
    logger.setLevel(logging.DEBUG)
    return logger

class KiwiLogger:
    def __init__(self, log_online=False, log_local=None, log_terminal=True):
        """Initializes a KiwiLogger object with optional loggers."""
        self.online_logger = get_online_logger("online_logger") if log_online else None
        self.local_logger = get_file_logger("file_logger", log_local) if log_local else None
        self.terminal_logger = get_terminal_logger("terminal_logger") if log_terminal else None

    def log(self, message, level='INFO', extra=None):
        """Logs a message with optional extra data and log level."""
        level = level.upper()
        inspect_data = self._get_inspect_data()

        if extra:
            inspect_data.update(extra)
            message_extra = ' | '.join([f"{k}: {v}" for k, v in extra.items()])
        else:
            message_extra = ""

        terminal_message = f"{message} | {message_extra}" if message and message_extra else f"{message}{message_extra}"
        file_message     = f"{message} | {message_extra}" if message and message_extra else f"{message}{message_extra}"
        logtail_message  = f"{message}"

        if message and message_extra:
            message = f"{message} | {message_extra}"
        elif message_extra:
            message = message_extra

        if level != "DEBUG":
            if self.online_logger:
                try:
                    self.online_logger.log(logging.getLevelName(level), logtail_message, extra=inspect_data)
                except ConnectionError as e:
                    # If Logtail server is unreachable, print error to terminal
                    print(f"Error connecting to Logtail: {e}")
            if self.local_logger:
                try:
                    self.local_logger.log(logging.getLevelName(level), file_message)
                except FileNotFoundError as e:
                    # If log file path is invalid, print error to terminal
                    print(f"Error creating file logger: {e}")
            if self.terminal_logger:
                self.terminal_logger.log(logging.getLevelName(level), terminal_message)
        else:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [DEBUG] {terminal_message}")

    def _get_inspect_data(self):
        """Returns a dictionary with data about the parent function."""
        frame = inspect.stack()[2]
        filename = os.path.basename(frame.filename)
        func_name = frame.function
        line_number = frame.lineno
        module_name = frame.frame.f_globals['__name__']
        return {
            'parentFileName': filename,
            'parentFuncName': func_name,
            'parentLineNumber': line_number,
            'parentModuleName': module_name,
        }
