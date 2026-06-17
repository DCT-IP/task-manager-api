import logging

try:
    result = 10 / 0
except ZeroDivisionError:
    # This automatically grabs the error details and the traceback
    logging.exception("An error occurred while calculating!")