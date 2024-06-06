from apps.scripts.email_verif import send_email
from apps.webapp.models import Borrowed
from apps.authentication.models import Users
from datetime import datetime
from flask import render_template


@crontab.job(minute="0", hour="10")
def send_email_reminder():
    # Loop through all borrowed items
    borrowed_items = Borrowed.query.all()
    for item in borrowed_items:
        # Check if return date is in less then 1 week
        time_left = item.estimated_return_date - datetime.now().timestamp()
        if time_left < 604800:
            # Send email to user
            user_id = item.user_id
            user = Users.query.filter_by(id=user_id).first()
            email = user.email

            return_date = item.estimated_return_date.strftime('%d-%m-%Y')
            html = render_template('app/email_reminder.html', return_date=return_date, time_left=int(time_left))
            send_email(email, "Return reminder", html)
        
        # Check if return date is tomorrow
        if time_left < 86400:
            # Send email to user
            user_id = item.user_id
            user = Users.query.filter_by(id=user_id).first()
            email = user.email

            return_date = item.estimated_return_date.strftime('%d-%m-%Y')
            html = render_template('app/email_reminder.html', return_date=return_date, time_left=int(time_left))
            send_email(email, "Return reminder", html)

        # Check if return date is passed
        if time_left <= 0:
            # Send email to user
            user_id = item.user_id
            user = Users.query.filter_by(id=user_id).first()
            email = user.email

            timestamp = datetime.fromtimestamp(int(item.estimated_return_date)).strftime('%d-%m-%Y')
            html = render_template('app/email_reminder.html', timestamp=timestamp)
            send_email(email, "Return reminder", html)