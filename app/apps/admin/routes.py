from apps.admin import blueprint
from flask import current_app, render_template, request

@blueprint.route('/login')
def admin_login():
    return render_template('app/admin-login.html')