from flask import Blueprint, render_template, session, request
import pygal as pl
from pygal.style import CleanStyle, LightenStyle
from pygal.style import Style
import locale

# Imports da modulos do app
from app.application import db

# Import das Models da Aplicação
from app.models.ciss.views import StokyMetasView as Metas
from app.models.ciss.cadastros import ClienteFornecedor as Vendedor

bp = Blueprint('bp', __name__)
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


@bp.route('/')
def index():
    return render_template('login.html')

