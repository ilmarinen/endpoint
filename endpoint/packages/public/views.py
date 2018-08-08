from flask import Blueprint, render_template
from flask_login import current_user, login_required
from endpoint.lib.http import no_cache


bp = Blueprint('public_views', __name__, template_folder='templates')


@bp.route('/')
@no_cache
def index():
    return render_template('public/index.html', title='Latest Plane Crash')
