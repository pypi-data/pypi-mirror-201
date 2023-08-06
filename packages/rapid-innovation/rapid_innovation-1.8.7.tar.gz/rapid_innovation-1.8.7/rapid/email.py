import os
import re
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .app.exceptions.email_exception import (
    InvalidEmailSubject,
    InvalidEmailReceiverAddress,
    InvalidEmailBody
)

from .app.helpers.validator import is_valid_email


class RapidEmailNotificationSMTP:
    """
       A class for sending email notifications using SMTP.
    """

    def __init__(self, smtp_sender_email, smtp_password):
        """
            Initializes the RapidEmailNotificationSMTP object.

            Parameters:
            smtp_sender_email (str): the email address of the SMTP sender
            smtp_password (str): the password for the SMTP sender's email account
        """
        self.smtp_sender_email = smtp_sender_email
        self.smtp_password = smtp_password

    def add_cc(self, cc):
        """
            Adds a list of email addresses to the CC field of the email.

            Parameters:
            cc (list): a list of email addresses

            Returns:
            str: a comma-separated string of valid email addresses
        """
        if type(cc) != list:
            raise InvalidEmailReceiverAddress('Invalid cc"s receiver address.')

        cc = [i for i in cc if is_valid_email(i)]
        return ', '.join(cc)

    def add_attachement(self, attach):
        """
            Adds an attachment to the email.

            Parameters:
            attach (str): the path to the file to be attached

            Returns:
            MIMEBase: a MIMEBase object representing the attachment
        """
        if type(attach) != str:
            print(f'Invalid attach file. {attach}')
            return False

        if not os.path.exists(attach):
            print(f'Invalid attach file. {attach}')
            return False

        # Open the file as binary mode
        with open(attach, 'rb') as file:
            attach_file = file.read()

        mime_base_payload = MIMEBase('application', 'octate-stream')
        mime_base_payload.set_payload(attach_file)

        # encode the attachment
        encoders.encode_base64(mime_base_payload)

        file_name = attach.split('/')[-1]

        # add payload header with filename
        mime_base_payload.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

        return mime_base_payload

    def send_email(self, to, subject, content, cc=None, attach=None):

        """
            Sends an email notification.

            Parameters:
            to (list): a list of email addresses to receive the email (mandatory)
            subject (str): the email subject (mandatory)
            content (str): the email body (mandatory)
            cc (list): a list of email addresses to CC on the email (optional)
            attach (str): the path to the file to be attached (optional)

            Returns:
            bool: True if the email was sent successfully
        """

        try:

            if not isinstance(to, list):
                raise InvalidEmailReceiverAddress('Invalid to receiver address.')

            # filter out invalid email addresses
            to = [i for i in to if is_valid_email(i)]

            mime_multipart_obj = MIMEMultipart('alternative')
            mime_multipart_obj['From'] = self.smtp_sender_email

            if not isinstance(subject, str):
                raise InvalidEmailSubject('Invalid subject.')
            mime_multipart_obj['Subject'] = subject

            mime_multipart_obj['To'] = ', '.join(to)
            receiver_email_id = to

            if cc:
                mime_multipart_obj['Cc'] = self.add_cc(cc)
                receiver_email_id += cc

            if not isinstance(content, str):
                raise InvalidEmailBody('Invalid email body.')

            mime_multipart_obj.attach(MIMEText(content, 'plain'))

            if attach:
                response_attach_file = self.add_attachement(attach)
                if response_attach_file:
                    mime_multipart_obj.attach(response_attach_file)

            # Connect to the SMTP server
            session = smtplib.SMTP('smtp.gmail.com', 587)

            # enable security
            session.starttls()

            # login with mail_id and password
            session.login(self.smtp_sender_email, self.smtp_password)

            mime_multipart_text = mime_multipart_obj.as_string()

            session.sendmail(self.smtp_sender_email, receiver_email_id, mime_multipart_text)

            session.quit()

            print(f"Email send successfully.")

        except Exception as e:
            raise e

        return True

