"""
Implements the logging configuration.
Simple configurator for the python logging package that allows simultaneous file and shell logging.
"""
import logging
from io import StringIO
from pathlib import Path

from .file_log_formatter import UncoloredFileLogFormatter
from .shell_log_formatter import ColoredShellLogFormatter


def setup_root_logger(shell_logging=True, file_logging=True, shell_log_lvl="info",
                      file_log_lvl="debug", logfile=Path('run.log')) -> None:
    """
    Sets up the root logger, so every created logger inherits the desired configuration.
    :param shell_logging: Enable/disable logging to STDOUT
    :param file_logging: Enable/disable logging to logfile
    :param shell_log_lvl: Severity threshold of shell logging
    :param file_log_lvl: Severity threshold of file logging
    :param logfile: Path to the logfile
    """
    logger = logging.getLogger()
    logging.root.setLevel(logging.NOTSET)

    if shell_logging:
        shell = logging.StreamHandler()
        shell.setLevel(shell_log_lvl.upper())
        color_dict = ColoredShellLogFormatter.SHELL_COLORS
        shell_format = ColoredShellLogFormatter(color_dict, '{message}', style='{')
        shell.setFormatter(shell_format)
        logger.addHandler(shell)

    if file_logging:
        logfile.parent.mkdir(parents=True, exist_ok=True)
        file = logging.FileHandler(logfile, mode='w')
        file.setLevel(file_log_lvl.upper())
        file_format = UncoloredFileLogFormatter(
            '{asctime} - {process} - {name} - {levelname} - {message}', style='{')
        file.setFormatter(file_format)
        logger.addHandler(file)


def buffer_log() -> StringIO:
    """
    Allows to buffer log before the setup function is used to configure the logging process.
    Buffered log is formatted by logging.basicConfig, buffered and can be logged after the logging
    has been set up.
    :return: Buffer storing the initial log
    """
    buffer = StringIO()
    logging.basicConfig(stream=buffer, level=logging.NOTSET)
    return buffer
