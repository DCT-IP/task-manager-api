import logging

logging.basicConfig(
    filename="app.log",  # Saves logs to a file named app.log
    filemode="a",  # 'a' means append to the file; 'w' would overwrite it every run
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("The user logged in successfully.")
logging.error("Failed to connect to the database.")