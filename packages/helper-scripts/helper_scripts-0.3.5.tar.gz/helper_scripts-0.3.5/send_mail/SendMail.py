from email.mime.base import MIMEBase
from os import error
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from petl.transform import headers
from database_handler import Helpers
from database_handler import DB
from database_handler import config as CONFIG
import pandas as pd
import petl as etl
from os import path

helpers = Helpers()

config = CONFIG('.config.ini', 'email_server')
params = config.read_config()


class SendMail:
     def send_email(self, email_message: str, subject :str,email_recepients:list,file_attachments = []):
        try:
            port = params['port']
            smtp_server = params['smtp_server']
            sender_email = params['sender_email']
            #sender_username = params['sender_username']
            login_email = params['sender_username']
            password = params['password']
            platform = params['platform']
            Bcc = ''

            message = MIMEMultipart()
            message['Subject'] = '%s' % (subject)
            message['From'] = sender_email
            message['To'] = ", ".join(email_recepients)
            message['Cc'] = None
            #message['Bcc'] = ", ".join(Bcc)
            # exit(print(etl.todataframe(Bcc)))

            html = '''
            <html>
            <head></head>
            <body>
            <p>Hello Team.
            <br> 
            %s 
            </p>
            </body>
            </html>
            ''' %(email_message)

            message.attach(MIMEText(html, 'html'))
            if file_attachments is not None or len(file_attachments) > 0:
                for filename in file_attachments:
                    if path.isdir(path.split(filename)[0]):
                        filenamex = path.split(filename)[-1]
                    else:
                        filenamex = filename
                    with open(filename, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)

                    part.add_header(
                        'Content-Disposition',
                        f'attachmen; filename= {filenamex} ',
                    )

                    message.attach(part)

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                print('sending mail started.....')
                # server.set_debuglevel(1)
                # server.ehlo()
                server.starttls(context=context)
                # server.ehlo()
                server.login(login_email, password)
                server.sendmail(sender_email, (email_recepients),
                                message.as_string())
                print('sending mail ended.....')
        except Exception as ex:
            raise ex