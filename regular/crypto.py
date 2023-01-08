from flask import Blueprint


bp = Blueprint('crypto', __name__, url_prefix='/crypto')


@bp.route('/')
def index():
    return 'crypto'
