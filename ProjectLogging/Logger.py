#!/usr/bin/env python3
# @author   Markus Kösters

import logging
import os.path
import typing


class Logger:
    """
    Class for configuring and managing logging functionality in an application.

    Provides capabilities to set up logging to files and the console, apply consistent
    formatter styles, and manage log file storage. This is useful for tracking application
    behavior, debugging, and storing runtime details. Includes utility to delete existing
    log files to maintain storage limits.

    :ivar DEFAULT_LOG_FILE: The default log file path if no custom file is specified.
    :type DEFAULT_LOG_FILE: str
    """
    DEFAULT_LOG_FILE = './MainLog.log'

    def __init__(self, name: str, logFile: str = './MainLog.log', logLevel: int = logging.DEBUG, consoleOutput: bool = True):
        if not logFile.endswith('.log'):
            logFile += '.log'
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logLevel)
        formatter: logging.Formatter = self.__setupFormatter(name)
        self.__setupFileHandler(logLevel, logFile, formatter, self.__logger)
        if consoleOutput:
            self.__setupConsoleHandler(logLevel, formatter, self.__logger)

    @staticmethod
    def __setupConsoleHandler(loglevel: int, formatter: logging.Formatter, logger: logging.Logger) -> None:
        """
        Method for setting up a console-log-handler.
        :param loglevel: Defines which log messages shall be streamed to the console.
        :param formatter: Defines the style of the log-messages in the console.
        :param logger: The logger that this console-streamer is being attached to.
        """
        consoleHandler: logging.StreamHandler = logging.StreamHandler()
        consoleHandler.setLevel(loglevel)
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

    @staticmethod
    def __setupFileHandler(logLevel: int, logFile: str, formatter: logging.Formatter, logger: logging.Logger) -> None:
        """
        Method for creating a file-handler for the logging.
        :param logLevel: Defines which log messages shall be stored into the log-file.
        :param formatter: Defines the style of the log-messages in the log-file.
        :param logFile: The log-file that the logs shall be stored in. Base-path is the "ProjectLogging" package.
        """
        fileHandler: logging.FileHandler = logging.FileHandler(os.path.join(os.path.dirname(__file__), logFile))
        fileHandler.setLevel(logLevel)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    @staticmethod
    def __setupFormatter(name: str) -> logging.Formatter:
        """
        Method defining the format of the logs.
        :return: Formatter, that will be used to set up the style of the logging.
        """
        return logging.Formatter('%(asctime)s - [%(levelname)s][%(name)s]: %(message)s\t',
                                 datefmt='%d-%m-%Y %H:%M:%S')

    @property
    def getLogger(self) -> logging.Logger:
        """
        Provides a property method to access the private logger instance.

        This property grants read-only access to the internally maintained
        logger instance, which may be used for logging purposes within the
        class or by external consumers.

        :return: The private logger instance of the class.
        :rtype: Logger
        """
        return self.__logger

    @staticmethod
    def __deleteExistingLogFiles() -> None:
        """
        Deletes all existing log files in the directory of the current script.

        This static method scans the directory where the current Python script resides
        and identifies files with a `.log` extension. For each identified log file, the
        file is removed from the filesystem. This operation permanently deletes the log
        files and cannot be undone.

        :raises FileNotFoundError: If a log file to be deleted does not exist at the
            moment of deletion (very rare case in a typical use).
        """
        logPath = os.path.dirname(__file__)
        files = os.listdir(logPath)
        for file in files:
            if file.endswith('.log'):
                os.remove(os.path.join(logPath, file))

    @staticmethod
    def __configureGlobalLogger(loggerName: str, logFile: str, logLevel: int, consoleOutput: bool) -> None:
        """
        Configures the global logger with the specified settings to enable centralized
        logging for the application. The logger is set to the specified log level and
        can optionally output logs to both a file and the console. This method ensures
        that duplicate handlers are avoided if the logger is already configured. A
        custom formatter is applied to all handlers.

        :param logFile: The file path where logs will be stored.
        :param logLevel: The logging level for the logger, such as logging.DEBUG
            or logging.ERROR.
        :param consoleOutput: A flag indicating whether logs should also be output
            to the console.
        :return: None
        """
        logger = logging.getLogger()  # Get the root logger (shared globally)
        logger.setLevel(logLevel)

        # Avoid duplicate handlers if the logger has already been configured
        if not logger.handlers:
            # Formatter for log messages
            formatter = Logger.__setupFormatter(loggerName)

            # Add file handler for logs
            Logger.__setupFileHandler(logLevel, logFile, formatter, logger)

            # Add optional console handler
            if consoleOutput:
                Logger.__setupConsoleHandler(logLevel, formatter, logger)

    """
    These methods are called when the module is imported.
    They ensure that the global logger is configured properly.
    And that old log files are deleted.
    """
    __deleteExistingLogFiles()