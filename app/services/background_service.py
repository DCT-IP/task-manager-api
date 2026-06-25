import time
from app.logger import logger

def send_fake_email(email: str):

    logger.info(
        f"Sending email to {email}"
    )

    time.sleep(5)

    logger.info(
        f"Email sent to {email}"
    )