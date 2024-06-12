from flask import Flask
from flask_mail import Mail, Message
from apps.config import Config
from flask import current_app


from apps.webapp.models import Borrowed
from apps.webapp.models import Product
from apps.authentication.models import Users
from datetime import datetime
from flask import render_template
from dateutil.relativedelta import relativedelta


# TEST
# from apps import mail
from apps import mail, scheduler


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


# @scheduler.task('cron', id='send_email_reminder', second='15')
def send_email_reminder():
    print("test")
    print("Now:", datetime.now())
    # Loop through all borrowed items
    borrowed_items = Borrowed.query.all()
    for borrow in borrowed_items:
        product_id = borrow.product_id
        item = Product.query.filter_by(id=product_id).first()
        # Time when item is supposed to be brought back
        return_date = borrow.estimated_return_date
        # Current time
        now = datetime.now()
        # Current time as unix timestamp
        now_timestamp = int(now.timestamp())
        # Convert Unix timestamp to datetime object
        exact_return_date = datetime.fromtimestamp(return_date)
        # Time left in seconds
        time_left = return_date - now_timestamp

        # Print the exact date and time
        print("Exact return date and time:", exact_return_date)
        # Format return date to only show date (day-month-year)
        formatted_return_date = exact_return_date.strftime('%d-%m-%Y')
        print("Formatted return date:", formatted_return_date)

        if time_left <= 0:
            delta = relativedelta(now, exact_return_date)
        else:
            delta = relativedelta(exact_return_date, now)
        months = delta.months
        weeks = delta.days // 7
        days = delta.days % 7
        hours = delta.hours

        # Get user name and email info from user that borrowed item
        user_id = borrow.user_id
        user = Users.query.filter_by(id=user_id).first()
        user_email = user.email
        user_email = "robinalmekinders@gmail.com"
        user_name = user.fullname

        # Get item info
        item_name = item.title

        # Check if return date is passed
        if time_left <= 0:
            message = (f"Time past return date: {months} month(s), {weeks} week(s), {days} day(s), {hours} hour(s)")
            print(f"Time past return date: {months} month(s), {weeks} week(s), {days} day(s), {hours} hour(s)")
            html = render_template('app/email_reminder.html', name=user_name, item=item_name,
                               return_date=formatted_return_date, message=message)
            # Send email to user
            send_email(user_email, "Return reminder", html)

        # Check if return date is in less then 1 week
        elif 518400 < time_left <= 604800 or 0 < time_left < 86400:
            message = (f"Time remaining: {months} month(s), {weeks} week(s), {days} day(s), {hours} hour(s)")
            print(f"Time remaining: {months} month(s), {weeks} week(s), {days} day(s), {hours} hour(s)")
            html = render_template('app/email_reminder.html', name=user_name, item=item_name,
                               return_date=formatted_return_date, message=message)
            # Send email to user
            send_email(user_email, "Return reminder", html)
