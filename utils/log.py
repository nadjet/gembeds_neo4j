import sys
import logging

LOGFILE = "/tmp/log.txt"

format = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'

# create logger with 'spam_application'
logger = logging.getLogger('')
logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)