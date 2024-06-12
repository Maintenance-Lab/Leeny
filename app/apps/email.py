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
from sqlalchemy.orm import undefer, joinedload
from apps import mail, scheduler, db


def send_email(to, subject, template):
    with scheduler.app.app_context():
        db.session.commit()
        msg = Message(
            subject=subject,
            sender=Config.MAIL_USERNAME,
            recipients=[to],
            html=template
        )
        mail.send(msg)
        return "Message sent!"


# Schedule the task for every morning at 9:00
@scheduler.task('cron', id='send_email_reminder', hour='9')
def send_email_reminder():
    with scheduler.app.app_context():
        with db.session() as session:
            # Eager load all borrowed items and related user and product
            borrowed_items = session.query(Borrowed).options(
                # undefer('product'),  # Load the product attribute eagerly
                # undefer('user'),     # Load the user attribute eagerly
                joinedload(Borrowed.product),
                joinedload(Borrowed.user)
            ).all()
            # Loop through all borrowed items
            for borrow in borrowed_items:
                # Merge the items in session with the ones from the database.
                borrow = session.merge(borrow)

                # Get item from borrowed item
                item = borrow.product
                # Time when item is supposed to be brought back
                return_date = borrow.estimated_return_date
                # Current time
                now = datetime.now()
                # Current time as unix timestamp
                now_timestamp = int(now.timestamp())
                # Time left in seconds
                time_left = return_date - now_timestamp

                # Convert return Unix timestamp to datetime object
                exact_return_date = datetime.fromtimestamp(return_date)
                # Format return date to only show date (day-month-year)
                formatted_return_date = exact_return_date.strftime('%d-%m-%Y')

                if time_left <= 0:
                    delta = relativedelta(now, exact_return_date)
                else:
                    delta = relativedelta(exact_return_date, now)
                months = delta.months
                weeks = delta.days // 7
                days = delta.days % 7
                hours = delta.hours

                # Get user name and email info from user that borrowed item
                user = borrow.user
                user_email = user.email
                user_name = user.fullname

                # Get item info
                item_name = item.title

                # Check if return date is passed
                if time_left <= 0:
                    message = (f"Allready past return date!!! Contact the Lab asap. \
                            Time past return date: {months} month(s), {weeks} week(s), \
                            {days} day(s), {hours} hour(s)")
                    html = render_template('app/email_reminder.html', name=user_name, item=item_name,
                                        return_date=formatted_return_date, message=message)
                    # Send email to user
                    send_email(user_email, "Return reminder", html)

                # Check if return date is in less then 1 week
                elif 518400 < time_left <= 604800:
                    message = (f"less then one week. Exact time remaining: {months} month(s),\
                            {weeks} week(s), {days} day(s), {hours} hour(s)")
                    html = render_template('app/email_reminder.html', name=user_name, item=item_name,
                                        return_date=formatted_return_date, message=message)
                    # Send email to user
                    send_email(user_email, "Return reminder", html)

                # Check if return date is in less then 1 day
                elif 0 < time_left < 86400:
                    message = (f"less then one week. Exact time remaining: {months} month(s),\
                            {weeks} week(s), {days} day(s), {hours} hour(s)")
                    html = render_template('app/email_reminder.html', name=user_name, item=item_name,
                                        return_date=formatted_return_date, message=message)
                    # Send email to user
                    send_email(user_email, "Return reminder", html)