import os
import sys
from logtail import LogtailHandler
import logging

class KiwiLogger:
    """
    A custom logger class that logs messages to Logtail, a local file, and/or the terminal.

    Usage:
    mlog = KiwiLogger(log_online=True, log_local=True, log_terminal=True)
    mlog('This is an INFO message.')  # Defaults to INFO level
    mlog('Something bad happened.', level='ERROR')
    mlog('Log message with structured logging.', level='INFO', extra={
        'item': "Orange Soda",
        'price': 100.00
    })
    """

    source_token = os.environ.get("LOGTAIL_SOURCE_TOKEN")

    def __init__(self, name=__name__, level='info', log_online=True, log_local=False, log_terminal=True):
        self.logger = self._setup_logger(name, level)
        self.logger.handlers = []
        self._setup_handler(log_online, log_local, log_terminal)

    def __call__(self, message, level='info', extra=None):
        if extra:
            for key, value in extra.items():
                message += f' | {key}: {value}'
            self.logger.log(self._get_level_number(level), message, extra=extra)
        else:
            self.logger.log(self._get_level_number(level), message)

    def _setup_logger(self, name, level):
        class NullHandler(logging.Handler):
            def emit(self, record):
                pass
        logger = logging.getLogger(name)
        logger.addHandler(NullHandler())
        logger.setLevel(self._get_level_number(level))
        return logger

    def _setup_handler(self, log_online, log_local, log_terminal):
        if log_online:
            online_handler = LogtailHandler(source_token=self.source_token)
            self.logger.addHandler(online_handler)

        if log_local:
            script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
            local_log_path = f"{script_name}.log"
            file_handler = logging.FileHandler(local_log_path)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if log_terminal:
            class StreamHandlerNoClose(logging.StreamHandler):
                def close(self):
                    # prevent StreamHandler from closing sys.stdout/stderr
                    pass

            stream_handler = StreamHandlerNoClose(sys.stdout)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def _get_level_number(self, level):
        level_number = getattr(logging, level.upper(), None)
        if not isinstance(level_number, int):
            level_number = logging.INFO
        return level_number
