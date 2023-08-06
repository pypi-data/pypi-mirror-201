import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter('%(asctime)s:%(lineno)d:%(module)s:%(funcName)s:%(levelname)s:%(message)s')
LOG_FILE = "morph_impl.log"
#s:%(name)
def get_console_handler():
   """
   The get_console_handler function creates a logging console handler and sets the formatter to FORMATTER.
   It returns the console_handler object.
   
   :return: A logging console handler
   :doc-author: Trelent
   """
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   """
   The get_file_handler function creates a file handler object that rotates the log files every midnight.
   It also sets the format of the log messages and returns this file handler object.
   
   :return: A timedrotatingfilehandler object
   :doc-author: Trelent
   """
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   """
   The get_logger function creates a logger object that is used to log messages.
   It also sets the logging level and attaches two handlers: one for the console,
   and another for a file. The function returns the logger object.
   
   :param logger_name: Name the logger
   :return: The logger object
   :doc-author: Trelent
   """
   logger = logging.getLogger(logger_name)
   if os.environ.get("loggingDebug") == "True":
      logger.setLevel(logging.DEBUG)
   else:
      logger.setLevel(logging.INFO) # better to have too much log than not enough
   if logger.handlers:
      logger.handlers =[] 
   # if os.environ.get("loggingDebug") == "True":
   #    logger.addHandler(get_console_handler())
   logger.addHandler(get_console_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger