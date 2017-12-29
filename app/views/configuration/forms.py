from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from app.core.forms import widgets as w


class ConfigForm(FlaskForm):
    """
    Formulario para alteração dos dados de Configuração do sistema
    """

    configId = HiddenField('ID', default=0)
    baseURL = StringField('URL Base', widget=w.GeInputWidget(), validators=[DataRequired()])

    submit = SubmitField('Atualizar')
