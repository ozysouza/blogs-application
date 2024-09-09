from dataclasses import dataclass, field

import logging
import os


@dataclass
class Log:
    """
    Sets up the logging configuration.

    Args:
        log_file (str): The name of the log file. Default is 'app.log'.
        log_dir (str): The directory where the log file will be created. Default is the current directory.
        console_level (int): The logging level for the console handler. Default is logging.INFO.
        file_level (int): The logging level for the file handler. Default is logging.DEBUG.
    """
    log_file: str = 'app.log'
    log_dir: str = 'logs'
    console_level: int = logging.INFO
    file_level: int = logging.DEBUG
    logger: logging.Logger = field(init=False, default=None)

    def __post_init__(self):
        """
         Initialize the logger after the dataclass is instantiated.
         This ensures that the logger is set up correctly.
         Ensure handlers are added only once
         """
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            self._setup_logger()

    def _setup_logger(self):
        """
        Sets up the logging configuration.
        """
        self.logger.setLevel(logging.DEBUG)  # Set the base logging level

        # Create and configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.console_level)
        console_format = logging.Formatter('%(levelname)s %(asctime)s - %(message)s', datefmt='%d/%b/%Y - %H:%M:%S')
        console_handler.setFormatter(console_format)

        # Ensure the log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Create and configure file handler
        file_handler = logging.FileHandler(f"{self.log_dir}/{self.log_file}")
        file_handler.setLevel(self.file_level)
        file_format = logging.Formatter('%(levelname)s %(asctime)s - %(message)s')
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
