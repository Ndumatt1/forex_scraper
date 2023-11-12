import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config


def send_mail(body):
    try:
        sender = config('SENDER')
        password = config('MAIL_PASSWORD')
        recipient = config('RECIPIENT')#.split(',')

        msg = MIMEMultipart()
        msg.attach(MIMEText(body))
        msg['Subject'] = "NEW SIGNAL ALERT!"
        msg['From'] = sender
        msg['Bcc'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient.split(','), msg.as_string())
            print("mail sent!")
    except Exception as e:
        print(f"Error sending mail {e}")
        return 'error'
