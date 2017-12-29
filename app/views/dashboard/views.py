from flask import Blueprint, render_template, session, request
from flask_login import login_required
import pygal as pl
from pygal.style import CleanStyle, LightenStyle
from pygal.style import Style

from app.views.dashboard.charts import getChartStyle, getHorizontalBar
from app.views.dashboard.charts import getHalfPie, getChartVendasAnoMes

from app.views.dashboard.data import getQtdadeNotas, getTotalVendido, getTotalCompraClientes
from app.views.dashboard.data import getVendasVendedores, getValLucroPeriodo
from app.views.dashboard.data import getValMeta, getTotalContasReceberPeriodo
from app.views.dashboard.data import getTotalContasPagarPeriodo, getProdutosPorQtdSaida
from app.views.dashboard.data import getProdutosEstoqueBaixo, getTotalVendasDoAnoPorMes

import calendar
import locale
import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@login_required
def index():
    # print(request.headers.get('User-Agent'))
    isMobile = (request.headers.get('User-Agent').find('Mobile') > 0)
    
    dataHoje = datetime.date.today()
    mes = dataHoje.month
    ano = dataHoje.year
    ultimoDiaMes = calendar.monthrange(ano, mes)[1]
    
    dataInicioMes = datetime.date(year=ano, month=mes, day=1)
    dataFimMes = datetime.date(year=ano, month=mes, day=ultimoDiaMes)

    # Valore usados no Tiles.html
    lucroDia = getValLucroPeriodo(dataHoje)
    lucroMes = getValLucroPeriodo(dataInicioMes, dataFinal=dataHoje)
    lucratividade = {
        'dia': lucroDia,
        'mes': lucroMes
    }

    # VERIFICADO
    vendasDia = getTotalVendido(dataHoje)
    vendasDia = locale.currency(vendasDia, grouping=True)
    vendasMes = getTotalVendido(dataInicioMes, dataFinal=dataHoje)
    vendasMes = locale.currency(vendasMes, grouping=True)
    valVendido = {
        'dia': vendasDia,
        'mes': vendasMes
    }

    # VERIFICADO
    notasDia = getQtdadeNotas(dataHoje)
    notasMes = getQtdadeNotas('{}-{}-01'.format(dataHoje.year, dataHoje.month), dataFinal=dataHoje)
    qtdNotas = {
        'dia': notasDia,
        'mes': notasMes
    }

    # VERIFICADO
    receberDia = getTotalContasReceberPeriodo(dataHoje)
    receberDia = locale.currency(receberDia, grouping=True)
    receberMes = getTotalContasReceberPeriodo(dataInicioMes, dataHoje)
    receberMes = locale.currency(receberMes, grouping=True)
    receber = {
        'dia': receberDia,
        'mes': receberMes
    }

    # VERIFICADO
    pagarDia = getTotalContasPagarPeriodo(dataHoje)
    pagarDia = locale.currency(pagarDia, grouping=True)
    pagarMes = getTotalContasPagarPeriodo(dataInicioMes, dataHoje)
    pagarMes = locale.currency(pagarMes, grouping=True)
    pagar = {
        'dia': pagarDia,
        'mes': pagarMes
    }

    # VERIFICADO
    estoqueBaixoTipoA = getProdutosEstoqueBaixo(tipoGiro='A')
    estoqueBaixoTipoAZerados = getProdutosEstoqueBaixo(tipoGiro='A', somenteZerados=True)
    estoqueBaixo = {
        'todos': estoqueBaixoTipoA.count(),
        'zerados': estoqueBaixoTipoAZerados.count()
    }

    # Valor Vendido por periodo
    metaTitulo = "Não existe Meta cadastrada para o período"
    maxValue = 1.0
    vendas = getTotalVendido(dataInicioMes, dataFinal=dataFimMes) 
    meta = getValMeta(12)
    if meta:
        metaTitulo = meta.descricao.capitalize()
        maxValue = float(meta.valTotalMeta)
        vendas = getTotalVendido(meta.dataInicial, dataFinal=meta.dataFinal)
    gauge = getHalfPie(metaTitulo, {'Total': {'value': vendas, 'max_value': maxValue, 'label': maxValue}} )

    # Qtdade de Notas por periodo
    qtdNotasGauge = getHalfPie('Qtdade de Notas Faturadas', {'Qtdade': {'value': notasDia, 'max_value': 30000}})

    # Valor Vendido por ano agrupado por mês
    anoPassado = ano - 1
    anoRetrasado = ano - 2    
    vendasAnoAtual = getTotalVendasDoAnoPorMes(ano)
    vendasAnoPassado = getTotalVendasDoAnoPorMes(anoPassado)
    vendasAnoRetrasado = getTotalVendasDoAnoPorMes(anoRetrasado)
    listaDeValores = [(str(ano), vendasAnoAtual), 
                      (str(anoPassado), vendasAnoPassado),
                      (str(anoRetrasado), vendasAnoRetrasado)]
    comparativoAnual = getChartVendasAnoMes(listaDeValores, isMobile=isMobile)

    # Vendas Externas por periodo
    # VERIFICADO
    vendasExternas = getVendasVendedores(dataInicioMes, dataFimMes, tipo='E')
    dataExternos = {}
    for vendedor in vendasExternas:
        dataExternos[vendedor.nome] = vendedor.total
    barChartsExternos = getHorizontalBar('Vendas por Vendedores Externos', dataExternos, isMobile=isMobile)

    # Vendas Internas por periodo
    # VERIFICADO
    vendasInternos = getVendasVendedores(dataInicioMes, dataFimMes, tipo='I')
    dataInternos = {}
    for vendedor in vendasInternos:
        dataInternos[vendedor.nome] = vendedor.total
    barChartsInternos = getHorizontalBar('Vendas por Vendedores Internos', dataInternos, isMobile=isMobile)

    meta_mes = locale.currency(maxValue, grouping=True)
    total_vendas = locale.currency(vendas, grouping=True)

    # Tabelas de Informações do Dashboard
    top10Produtos = getProdutosPorQtdSaida(dataInicioMes, dataFinal=dataHoje, limit=10)
    top10Clientes = getTotalCompraClientes(dataInicioMes, dataFinal=dataHoje, limit=10, convertToList=True)

    result = {
        'gauge': gauge,
        'notas': qtdNotasGauge,
        'barChartsExternos': barChartsExternos,
        'barChartsInternos': barChartsInternos,
        'total_vendas': total_vendas,
        'meta_mes': meta_mes,
        'qtdNotas': qtdNotas,
        'lucratividade': lucratividade,
        'valVendido': valVendido,
        'receber': receber,
        'pagar': pagar,
        'top10Produtos': top10Produtos,
        'top10Clientes': top10Clientes,
        'estoqueBaixo': estoqueBaixo,
        'comparativoAnual': comparativoAnual
    }
    return render_template('dashboard/main.html', **result)

