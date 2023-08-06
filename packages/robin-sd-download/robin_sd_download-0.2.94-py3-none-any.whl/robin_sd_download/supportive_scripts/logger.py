import logging
import os
import datetime

from robin_sd_download.supportive_scripts import yaml_parser

# Fetch the logfile location from config
config = yaml_parser.parse_config()

# Check if the config was parsed correctly
if config is None:
    raise Exception("Could not parse YAML config file")

log_file = config['log']['file']
app_name = config['static']['app_name']
log_dir = os.path.dirname(log_file)

# Check if log_file or app_name is exist in config
if log_file is None or app_name is None:
    raise Exception("log_file or app_name is not defined in config")

# Create the log directory if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging
amsterdam_tz = datetime.timezone(datetime.timedelta(hours=1), 'CET')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %z',
                    filename=log_file,
                    filemode='a')

logging.Formatter.converter = lambda *args: datetime.datetime.now(
    amsterdam_tz).timetuple()

logger = logging.getLogger(app_name)


def log(message: str, to_terminal: bool = False, log_level: str = 'info'):
    """Logs a message to a file and/or the terminal"""

    # Fail if the log level is not valid, it can only be 'debug', 'info', 'warning', or 'error'
    if log_level not in ['debug', 'info', 'warning', 'error']:
        raise ValueError(
            "log_level must be either 'debug', 'info', 'warning', or 'error'")

    if not isinstance(message, str):
        raise TypeError("message must be of type string")

    if not isinstance(to_terminal, bool):
        raise TypeError("to_terminal must be of type boolean")

    if log_level == 'debug':
        logger.debug(message)
    elif log_level == 'info':
        logger.info(message)
    elif log_level == 'warning':
        logger.warning(message)
    elif log_level == 'error':
        logger.error(message)

    if to_terminal:
        print(f"{datetime.datetime.now(amsterdam_tz).strftime('%Y-%m-%d %H:%M:%S %z')} - {log_level.upper()} - {message}")
