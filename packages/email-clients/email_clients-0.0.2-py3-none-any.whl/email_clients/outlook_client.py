from smtplib import SMTP
from email.message import EmailMessage

class OutlookClient:
    def __init__(self, email_address: str, password: str):
        self.server = SMTP('smtp-mail.outlook.com',port=587)
        self.server.starttls()
        self.server.login(email_address,password)
        self.email_address = email_address
        self.password = password     

    def send_mail(self,to_email_address: str, subject: str, message: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_address
        msg['To'] = to_email_address
        msg.set_content(message)
        self.server.send_message(msg,self.email_address,to_email_address)