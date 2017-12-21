from flask import Blueprint, render_template, request

# Import de Formularios
from app.views.compras.forms import FormEstoqueBaixo

# Import dos datas Usados
from app.views.compras.data import getProdutosEstoqueBaixo, getMarcasEstoqueBaixo


compras = Blueprint('compras', __name__)


@compras.route('/estoque-baixo', methods=['GET', 'POST'])
def listaProdutosEstoqueBaixo():
    form = FormEstoqueBaixo()
    produtos = None
    produtosToJson = None
    marcas = None

    if form.validate_on_submit():
        tipoGiro = form.tipoGiro.data
        zerados = form.zerados.data

        produtos, produtosToJson = getProdutosEstoqueBaixo(tipoGiro=tipoGiro, somenteZerados=zerados)

        marcas = getMarcasEstoqueBaixo(tipoGiro=tipoGiro, somenteZerados=zerados)
    
    content = {
        'form': form,
        'produtos': produtos,
        'produtosToJson': produtosToJson,
        'marcas': marcas
    }
    return render_template('compras/estoque_minimo.html', **content)