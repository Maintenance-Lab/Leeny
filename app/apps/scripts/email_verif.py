from flask import Flask
from flask_mail import Mail, Message
from apps.config import Config


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'Config.MAIL_USERNAME          # Sender Gmail address
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD          #  Generated App Password
# app.config['GMAIL_PASSWORD']= Config.GMAIL_PASS           #  Gmail Passwords
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


def send_email(to, subject, template):
    msg = Message(
        subject=subject,
        sender=Config.MAIL_USERNAME,
        recipients=[to],
        html=template
    )
    mail.send(msg)
    return "Message sent!"