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


@bp.route('client_info', methods=['POST'])
def client_info():
    if request.method == 'POST':
        if('screen_width' in request.form) and request.form['screen_width']:
            session['screen_width'] = request.form['screen_width']
    return '', 200


@bp.route('/')
def index():
    meta = 3800000.00
    label = locale.currency(meta, grouping=True)
    query = (db.func.sum(Metas.val_venda) + db.func.sum(Metas.val_devolucao)).label('total')
    vendas = db.session.query(query)
    vendas = vendas.filter(Metas.dt_movimento.between('2017-12-01', '2017-12-30')).first()

    config = pl.Config()
    config.title = 'Total de Vendas do Mês'
    config.show_legend = False
    config.human_readable = True
    # config.value_formatter = lambda x: locale.currency(x, grouping=True)
    config.half_pie = True
    config.inner_radius = 0.70
    # config.spacing = 120
    config.style = get_chart_style()

    gauge = pl.SolidGauge(config, value_formatter = lambda x: locale.currency(x, grouping=True))
    gauge.add('Total', [{'value': vendas.total, 'max_value': meta, 'label': 'Meta:{}'.format(label)}])

    qtdade_notas = get_qtdade_notas()

    notas_gauge = pl.SolidGauge(config, title="Qtdade de Notas Faturadas")
    notas_gauge.add('Qtdade', [{'value': qtdade_notas, 'max_value': 30000}])

    vendas_externas = get_vendas_vendedores(tipo='E')
    data = {}
    for v in vendas_externas:
        data[v.nome] = v.total
    
    bar_charts = get_horizontal_bar_chart('Vendas por Vendedores Externos', data)

    vendas_internas = get_vendas_vendedores(tipo='I')
    data_internas = {}
    for v in vendas_internas:
        data_internas[v.nome] = v.total
    
    bar_charts_interno = get_horizontal_bar_chart('Vendas por Vendedores Internos', data_internas)

    meta_mes = locale.currency(meta, grouping=True)
    total_vendas = locale.currency(vendas.total, grouping=True)
    return render_template('index.html', gauge=gauge.render_data_uri(), notas=notas_gauge.render_data_uri(), bar_charts=bar_charts,
                           bar_charts_interno=bar_charts_interno, total_vendas=total_vendas, meta_mes=meta_mes)


def get_qtdade_notas():
    query_filter = Metas.dt_movimento.between('2017-12-01', '2017-12-30')
    qtdade_notas = Metas.query.filter(query_filter).count()
    return qtdade_notas


def get_vendas_vendedores(tipo=None):
    query_total = (db.func.sum(Metas.val_venda) + db.func.sum(Metas.val_devolucao)).label('total')
    vendas_total = db.session.query(Metas.id_vendedor, Vendedor.nome, query_total)
    
    filter_periodo = (Metas.dt_movimento.between('2017-12-01', '2017-12-30'))
    vendas_total = vendas_total.filter(filter_periodo)
    vendas_total = vendas_total.filter(Vendedor.id_cli_for == Metas.id_vendedor)

    if(tipo == 'E'):
        vendas_total = vendas_total.filter(Vendedor.vendedor_externo == 'T')
    if(tipo == 'I'):
        vendas_total = vendas_total.filter(Vendedor.vendedor_externo == 'F')
    vendas_total = vendas_total.group_by(Metas.id_vendedor, Vendedor.nome)

    return vendas_total


def get_horizontal_bar_chart(title, data):
    config = pl.Config()
    config.legend_at_bottom = True
    config.value_formatter = lambda x: locale.currency(x, grouping=True)
    config.legend_box_size = 26
    # config.height = 1000
    config.style = get_chart_style()

    bar_chart = pl.HorizontalBar(config)
    bar_chart.title = title
    if isinstance(data, dict):
        for key, value in data.items():
            nome = key.split()
            nome = '{} {}'.format(nome[0], nome[-1])
            bar_chart.add(nome, value)
    
    return bar_chart.render_data_uri()


def get_chart_style():
    custom_style = Style(
        value_colors='blue',
        plot_background='#FBFBFC',
        font_family='googlefont:Barlow'
    )
    screen_width = int(session.get('screen_width')) if session.get('screen_width') else 1900

    if(screen_width <= 700 ):
        custom_style.value_font_size = 35
        custom_style.title_font_size = 35
        custom_style.tooltip_font_size = 35
        print(700)
    elif(screen_width <= 990):
        custom_style.value_font_size = 35
        custom_style.title_font_size = 35
        custom_style.tooltip_font_size = 35
        print(990)
    elif(screen_width <= 1400):
        custom_style.value_font_size = 35
        custom_style.title_font_size = 35
        custom_style.tooltip_font_size = 35
        print(1400)
    else:
        custom_style.value_font_size = 35
        custom_style.title_font_size = 35
        custom_style.tooltip_font_size = 35
        print(1900)
    
    print(custom_style.title_font_size)
    return custom_style

