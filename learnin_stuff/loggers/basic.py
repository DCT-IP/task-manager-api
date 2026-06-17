import logging

# 1. Configure the logging system
logging.basicConfig(
    level=logging.DEBUG,  # Change default from WARNING to DEBUG to see all logs
    format="%(asctime)s - %(levelname)s - %(message)s",  # Customize what information is shown
)

# 2. Log some messages
logging.debug("This is a debug message (helpful for fixing code).")
logging.info("This is an info message (tracked application flow).")
logging.warning("This is a warning message (something looks fishy!).")
logging.error("This is an error message (something actually broke).")
logging.critical("This is a critical message (the whole system is crashing!).")