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
    print(Config.MAIL_DEFAULT_SENDER, Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=Config.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)
