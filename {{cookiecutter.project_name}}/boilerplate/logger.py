import configparser
import inspect
import logging
from typing import Any

from rich.logging import RichHandler
from rich.traceback import Traceback
from stgpytools import SPath

__all__: list[str] = [
    "Log"
]


class _Logger:
    """A class for logging messages."""

    _logger: logging.Logger
    """The logger for the class."""

    def __init__(self, name: str = "", level: int | None = None):
        """Initialize the logger with the given name and level."""

        self._logger = self._setup_logger(name, level)

    def _get_logging_level(self):
        """Get the logging level from the vsmuxtools config file."""

        config = configparser.ConfigParser()
        config_file = SPath('config.ini')

        if not SPath(config_file).exists():
            return logging.INFO

        config.read(config_file)
        debug = config.getboolean('settings', 'debug', fallback=False)

        return logging.DEBUG if debug else logging.INFO

    def _setup_logger(self, name: str = "", level: int | None = None) -> logging.Logger:
        """Set up the logger with the given name and level."""

        name = name or "encode_boilerplate_logger"
        level = level or self._get_logging_level()

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            FORMAT = "%(name)s | %(message)s"
            handler = RichHandler(markup=True, omit_repeated_times=False, show_path=False)

            # Configure the logger
            logging.basicConfig(format=FORMAT, datefmt="[%X]", handlers=[handler])

        return logger

    @staticmethod
    def _format_msg(msg: str, caller: Any) -> str:
        """Formatting taken from vsmuxtools."""

        if caller and not isinstance(caller, str):
            caller = caller.__class__.__qualname__ if hasattr(caller, "__class__") \
                and caller.__class__.__name__ not in ["function", "method"] else caller

            caller = caller.__name__ if not isinstance(caller, str) else caller

        return msg if caller is None else f"[bold]{caller}:[/] {msg}"

    def _log_with_caller(
        self, level: int, message: str, caller: Any = None, exc: Exception | None = None
    ) -> None:
        """Format and log the message with the caller's name."""

        caller = inspect.stack()[1].function

        msgs = list[str]()

        if exc and level >= logging.ERROR:
            msgs += [f"{Traceback.from_exception(exc, exc, None)}"]  # type:ignore[arg-type]

        msgs += [self._format_msg(message, caller)]

        full_message = "\n".join(msgs)

        match level:
            case logging.DEBUG:
                self._logger.debug(full_message)
            case logging.INFO:
                self._logger.info(full_message)
            case logging.WARNING:
                self._logger.warning(full_message)
            case logging.ERROR:
                self._logger.error(full_message)
            case logging.CRITICAL:
                self._logger.critical(full_message)
            case _:
                self._logger.info(full_message)

    def debug(self, message: str, caller: Any) -> None:
        """Log a debug message with the caller's name."""

        self._log_with_caller(logging.DEBUG, message, caller)

    def info(self, message: str, caller: Any) -> None:
        """Log an info message with the caller's name."""

        self._log_with_caller(logging.INFO, message, caller)

    def warning(self, message: str, caller: Any) -> None:
        """Log a warning message with the caller's name."""

        self._log_with_caller(logging.WARNING, message, caller)

    def error(self, message: str, caller: Any) -> None:
        """Log an error message with the caller's name."""

        self._log_with_caller(logging.ERROR, message, caller)

    def critical(self, message: str, caller: Any) -> None:
        """Log a critical message with the caller's name."""

        self._log_with_caller(logging.CRITICAL, message, caller)

    # Aliases
    def warn(self, message: str, caller: Any) -> None:
        """Log a warning message with the caller's name."""

        self.warning(message, caller)

    def fatal(self, message: str, caller: Any) -> None:
        """Log a critical message with the caller's name."""

        self.critical(message, caller)

    def exception(self, message: str, caller: Any) -> None:
        """Log an error message with the caller's name."""

        self.error(message, caller)


Log = _Logger()
# The logger instance.
