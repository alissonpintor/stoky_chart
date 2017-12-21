from flask import Blueprint, render_template, session, request
import pygal as pl
from pygal.style import CleanStyle, LightenStyle
from pygal.style import Style

from app.views.dashboard.charts import getChartStyle, getHorizontalBar
from app.views.dashboard.charts import getHalfPie

from app.views.dashboard.data import getQtdadeNotas, getTotalVendido, getTotalCompraClientes
from app.views.dashboard.data import getVendasVendedores, getValLucroPeriodo
from app.views.dashboard.data import getValMeta, getTotalContasReceberPeriodo
from app.views.dashboard.data import getTotalContasPagarPeriodo, getProdutosPorQtdSaida
from app.views.dashboard.data import getProdutosEstoqueBaixo

import locale
import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
def index():
    dataHoje = datetime.date.today()
    dataInicioMes = datetime.date(year=dataHoje.year, month=dataHoje.month, day=1)

    # Valore usados no Tiles.html
    lucroDia = getValLucroPeriodo(dataHoje)
    lucroMes = getValLucroPeriodo(dataInicioMes, dataFinal=dataHoje)
    lucratividade = {
        'dia': lucroDia,
        'mes': lucroMes
    }

    vendasDia = getTotalVendido(dataHoje)
    vendasDia = locale.currency(vendasDia, grouping=True)
    vendasMes = getTotalVendido(dataInicioMes, dataFinal=dataHoje)
    vendasMes = locale.currency(vendasMes, grouping=True)
    valVendido = {
        'dia': vendasDia,
        'mes': vendasMes
    }

    notasDia = getQtdadeNotas(dataHoje)
    notasMes = getQtdadeNotas('{}-{}-01'.format(dataHoje.year, dataHoje.month), dataFinal=dataHoje)
    qtdNotas = {
        'dia': notasDia,
        'mes': notasMes
    }

    receberDia = getTotalContasReceberPeriodo(dataHoje)
    receberDia = locale.currency(receberDia, grouping=True)
    receberMes = getTotalContasReceberPeriodo(dataInicioMes, dataHoje)
    receberMes = locale.currency(receberMes, grouping=True)
    receber = {
        'dia': receberDia,
        'mes': receberMes
    }

    pagarDia = getTotalContasPagarPeriodo(dataHoje)
    pagarDia = locale.currency(pagarDia, grouping=True)
    pagarMes = getTotalContasPagarPeriodo(dataInicioMes, dataHoje)
    pagarMes = locale.currency(pagarMes, grouping=True)
    pagar = {
        'dia': pagarDia,
        'mes': pagarMes
    }

    estoqueBaixoTipoA = getProdutosEstoqueBaixo(tipoGiro='A')
    estoqueBaixoTipoAZerados = getProdutosEstoqueBaixo(tipoGiro='A', somenteZerados=True)
    estoqueBaixo = {
        'todos': estoqueBaixoTipoA.count(),
        'zerados': estoqueBaixoTipoAZerados.count()
    }

    # Valor Vendido por periodo    
    meta = getValMeta(12)
    metaTitulo = meta.descricao.capitalize()
    maxValue = float(meta.valTotalMeta)
    vendas = getTotalVendido(meta.dataInicial, dataFinal=meta.dataFinal)
    gauge = getHalfPie(metaTitulo, {'Total': {'value': vendas, 'max_value': maxValue, 'label': maxValue}} )

    # Qtdade de Notas por periodo
    qtdNotasGauge = getHalfPie('Qtdade de Notas Faturadas', {'Qtdade': {'value': notasDia, 'max_value': 30000}})

    # Vendas Externas por periodo
    vendas_externas = getVendasVendedores(tipo='E')
    data = {}
    for v in vendas_externas:
        data[v.nome] = v.total    
    bar_charts = getHorizontalBar('Vendas por Vendedores Externos', data)

    # Vendas Internas por periodo
    vendas_internas = getVendasVendedores(tipo='I')
    data_internas = {}
    for v in vendas_internas:
        data_internas[v.nome] = v.total
    bar_charts_interno = getHorizontalBar('Vendas por Vendedores Internos', data_internas)

    meta_mes = locale.currency(maxValue, grouping=True)
    total_vendas = locale.currency(vendas, grouping=True)

    # Tabelas de Informações do Dashboard
    top10Produtos = getProdutosPorQtdSaida(dataInicioMes, dataFinal=dataHoje, limit=10)
    top10Clientes = getTotalCompraClientes(dataInicioMes, dataFinal=dataHoje, limit=10, convertToList=True)

    result = {
        'gauge': gauge,
        'notas': qtdNotasGauge,
        'bar_charts': bar_charts,
        'bar_charts_interno': bar_charts_interno,
        'total_vendas': total_vendas,
        'meta_mes': meta_mes,
        'qtdNotas': qtdNotas,
        'lucratividade': lucratividade,
        'valVendido': valVendido,
        'receber': receber,
        'pagar': pagar,
        'top10Produtos': top10Produtos,
        'top10Clientes': top10Clientes,
        'estoqueBaixo': estoqueBaixo
    }
    return render_template('dashboard/main.html', **result)

