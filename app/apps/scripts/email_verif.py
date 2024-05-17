from flask import Flask
from flask_mail import Mail, Message
from apps.config import Config


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'leeny.maintenance@gmail.com'     # Sender Gmail address
app.config['MAIL_PASSWORD'] = 'xzou bejm kwlg bsgy'             #  Generated App Password
# app.config['EMAIL_PASS']='1hva2leeny3uva'                       #  Gmail Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


def send_email(to, subject, template):
    print(subject, Config.MAIL_USERNAME, to, template)
    msg = Message(
        subject=subject,
        sender=Config.MAIL_USERNAME,
        recipients=[to],
        html=template
    )
    mail.send(msg)
    return "Message sent!"