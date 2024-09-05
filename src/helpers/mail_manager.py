import os
import smtplib as mail

from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.helpers.log import Log


@dataclass(frozen=True)
class MailManager:
    email_sender: str = os.getenv('EMAIL_ADDRESS')
    email_passwd: str = os.getenv('EMAIL_PASSWORD')

    def send_email(self, name: str, email: str, number: str, body: str) -> None:
        logger = Log().logger
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = self.email_sender
            msg['Subject'] = f"New message from {name}"

            message = (
                f"Email: {email}\n\n"
                f"Phone number: {number}\n\n"
                f"Message: {body}"
            )
            msg.attach(MIMEText(message, 'plain'))

            with mail.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=self.email_sender, password=self.email_passwd)
                connection.send_message(msg)
                logger.info("Email sent successfully.")
        except Exception as e:
            logger.error(f"{e}")
