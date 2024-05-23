from flask import Flask
from flask_mail import Mail, Message
from apps.config import Config
from flask import current_app

from flask import current_app as app
from apps import mail


def send_email(to, subject, template):
    with current_app.app_context():
        msg = Message(
            subject=subject,
            sender=Config.MAIL_USERNAME,
            recipients=[to],
            html=template
        )
        mail.send(msg)
        return "Message sent!"