from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from app.core.forms import widgets as w


class FormEstoqueBaixo(FlaskForm):
    """
    Formulario para validar os dados informados na tela
    de listagem de produtos com estoque baixo
    """
    choices = [('', ''), ('A', 'Alto'), ('M', 'Médio'), ('B', 'Baixo')]
    tipoGiro = SelectField('Tipo de Giro', choices=choices, coerce=str, widget=w.GeSelectWidget())

    choicesZerados = [('S', 'Sim'), ('', 'Não')]
    zerados = SelectField('Somente Zerados', choices=choicesZerados, coerce=str, widget=w.GeSelectWidget())

    submit = SubmitField('Buscar')