from flask import Blueprint, render_template


account = Blueprint('account', __name__)


@account.route('/')
def index():
    return render_template('account/main.html')