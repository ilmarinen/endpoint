from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_admin.contrib import sqla
import forms
import manage


bp = Blueprint('user_views', __name__, template_folder='templates')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('public_views.index'))
    elif login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = manage.get_user_by_username(username)
        if manage.verify_user_password(user, password):
            login_user(user, remember=True)
            return redirect(url_for('public_views.index'))

    return render_template('user/login.html', form=login_form)


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('user_views.login'))


class AuthModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
