from flask import Blueprint, render_template

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:id>')
def profile(id):
    return render_template('profile.html')