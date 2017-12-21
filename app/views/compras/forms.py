from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class FormEstoqueBaixo(FlaskForm):
    """
    Formulario para validar os dados informados na tela
    de listagem de produtos com estoque baixo
    """
    choices = [('', ''), ('A', 'Alto'), ('M', 'Médio'), ('B', 'Baixo')]
    tipoGiro = SelectField('Tipo de Giro', choices=choices, coerce=str)

    choicesZerados = [('S', 'Sim'), ('', 'Não')]
    zerados = SelectField('Somente Zerados', choices=choicesZerados, coerce=str)

    submit = SubmitField('Buscar')