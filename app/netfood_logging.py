
import logging
from netfood_bdd import fetchBDD, executeBDD
from netfood_logginglevel import netfoodLogLevel

config = {}
file = "netfood.log"

logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(file)
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


def log_setConfig(config_file):
    global config
    global logLevel
    global file
    config = config_file
    logLevel = config['logLevel']
    file = config['logFile']


def log_setFile(log_file):
    global file
    file = log_file


def log_setLevel(log_level):
    global logLevel
    logLevel = log_level


def log_debug(message):
    """
    Create a debug level message
    :param str message: Message to log
    :return: nothing
    """
    if logLevel <= int(netfoodLogLevel.DEBUG):
        log_store(netfoodLogLevel.DEBUG, message)


def log_info(message):
    """
    Create an info level message
    :param str message: Message to log
    :return: nothing
    """
    if logLevel <= int(netfoodLogLevel.INFO):
        log_store(netfoodLogLevel.INFO, message)


def log_warning(message):
    """
    Create a warning level message
    :param str message: Message to log
    :return: nothing
    """
    if logLevel <= netfoodLogLevel.WARNING:
        log_store(netfoodLogLevel.INFO, message)


def log_error(message):
    """
    Create an error level message
    :param str message: Message to log
    :return: nothing
    """
    if logLevel <= netfoodLogLevel.ERROR:
        log_store(netfoodLogLevel.ERROR, message)


def log_fatal(message):
    """
    Create a fatal level message
    :param str message: Message to log
    :return: nothing
    """
    if logLevel <= netfoodLogLevel.FATAL:
        log_store(netfoodLogLevel.INFO, message)


def log_log(log_level, message):
    """
    Create a fatal level message
    :param netfoodLogLevel log_level: Log Level
    :param str message: Message to log
    :return: nothing
    """
    if logLevel <= log_level:
        if logLevel == netfoodLogLevel.DEBUG:
            log_debug(message)
        elif logLevel == netfoodLogLevel.INFO:
            log_info(message)
        elif logLevel == netfoodLogLevel.WARNING:
            log_warning(message)
        elif logLevel == netfoodLogLevel.ERROR:
            log_error(message)
        elif logLevel == netfoodLogLevel.FATAL:
            log_fatal(message)
        else:
            log_error("Call to unknown log level with message: "+message)


def log_store(log_level, message):
    """
    Store
    :param log_level: Message level
    :param message: Message to log
    :return: nothing
    """
    logger.log(log_level, message)
    level = ""
    level_logging = logging.DEBUG
    if log_level == netfoodLogLevel.DEBUG:
        level = "debug"
        level_logging = logging.DEBUG
    elif log_level == netfoodLogLevel.INFO:
        level = "info"
        level_logging = logging.INFO
    elif log_level == netfoodLogLevel.WARNING:
        level = "warning"
        level_logging = logging.WARNING
    elif log_level == netfoodLogLevel.ERROR:
        level = "error"
        level_logging = logging.ERROR
    elif log_level == netfoodLogLevel.FATAL:
        level = "fatal"
        level_logging = logging.FATAL

    logger.log(level_logging, message)

    executeBDD ( "db.log.insertOne ({'level' : '{message}','message':'{message}'})" , config )

 


def log_getAll():
    """
    Get all records from database
    :return: List of records
    """
    records = fetchBDD ("db.log.insertOne.find().sort({ joining_date: 1})", config)
    return records

