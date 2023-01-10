import pyupbit
from flask import Blueprint

from regular.util.fileio import json_load


bp = Blueprint('crypto', __name__, url_prefix='/crypto')


config = json_load('regular/config.json')
access_key = config['access_key']
secret_key = config['secret_key']
upbit = pyupbit.Upbit(access_key, secret_key)


@bp.route('/')
def index():
    return 'crypto'
