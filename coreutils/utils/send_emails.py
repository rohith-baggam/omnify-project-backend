from core.settings import logger
from core import settings
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging

# Configure logger with application name
logger = logging.LoggerAdapter(logger, {"app_name": "send_an_email"})


def send_an_email(
    receiver_email,
    subject,
    body,
    file_name=None,
    file_path=None,
    login_user_name=None,
    login_user_pass=None,
):
    """
    Sends an email with optional attachments.

    Args:
        receiver_email (list): List of recipient email addresses.
        subject (str): Email subject.
        body (str): Email body (HTML format).
        file_name (str, optional): Name of the file attachment. Defaults to None.
        file_path (str, optional): Full path to the file attachment. Defaults to None.
        login_user_name (str, optional): SMTP username for authentication. Defaults to None.
        login_user_pass (str, optional): SMTP password for authentication. Defaults to None.

    Returns:
        tuple: (bool, str) indicating success or failure message.
    """
    try:
        # Create an instance of MIMEMultipart for constructing the email
        msg = MIMEMultipart()
        msg["Subject"] = subject

        # Retrieve SMTP configuration from settings
        smtp_server: str = settings.SMTP_SERVER
        smtp_port: int = settings.SMTP_PORT
        msg["From"] = smtp_sender_email = settings.SMTP_SENDER_EMAIL
        smtp_password: str = settings.SMTP_PASSWORD

        # If custom login credentials are provided, override default SMTP settings
        if None not in [login_user_name, login_user_pass]:
            msg["From"] = smtp_sender_email = login_user_name
            smtp_password: str = login_user_pass

        logger.info(
            "SMTP Config: Server=%s, Port=%s, Sender=%s",
            smtp_server,
            smtp_port,
            smtp_sender_email,
        )

        # Attach the email body
        msg.attach(MIMEText(body, "html"))

        # Attach file if provided
        if file_path is not None:
            with open(file_path, "rb") as attachment:
                p = MIMEBase("application", "octet-stream")
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition", f"attachment; filename={file_name}")
                msg.attach(p)

        # Establish SMTP session
        if settings.EMAIL_CONNECTION == "TLS":
            s = smtplib.SMTP(smtp_server, smtp_port)
            logger.info("SMTP TLS connection established")
            # ? start TLS for security
            s.starttls()
            logger.info("TLS session started")
        else:
            s = smtplib.SMTP_SSL(smtp_server, smtp_port)
            logger.info("SMTP SSL connection established")
            logger.info("SSL session started")

        # Authenticate with the SMTP server
        s.login(smtp_sender_email, smtp_password)
        logger.info("SMTP authentication successful")

        # Set recipients
        for recipient in receiver_email:
            msg["To"] = recipient

        # Send email
        s.sendmail(
            from_addr=smtp_sender_email, to_addrs=receiver_email, msg=msg.as_string()
        )
        logger.info("Email successfully sent to %s", receiver_email)

        # Terminate the SMTP session
        s.quit()
        return True, "Success"

    except Exception as e:
        logger.error("Email sending failed: %s", str(e))
        return False, str(e)
