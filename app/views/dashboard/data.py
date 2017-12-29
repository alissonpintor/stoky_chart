import locale
import datetime

# Imports da modulos do app
from app.application import db

# Import das Models da Aplicação
from app.models.ciss.views import StokyMetasView as MetasVendas
from app.models.ciss.views import ViewContasReceber as Receber
from app.models.ciss.views import ViewContasPagar as Pagar
from app.models.ciss.views import ViewProduto as Produto
from app.models.ciss.views import ViewSaldoProduto as SaldoProduto
from app.models.ciss.cadastros import ClienteFornecedor as Vendedor
from app.models.ciss.vendas import Metas, MetasPrevisao
from app.models.ciss.compras import Notas, SugestaoCompra as Sugestao
from app.models.ciss.estoques import EstoqueAnalitico as Estoque


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


# VERIFICADO
def getTotalVendido(dataInicial, dataFinal=None):
    query = (db.func.sum(MetasVendas.val_venda) + db.func.sum(MetasVendas.val_devolucao)).label('total')
    vendas = db.session.query(query)

    if dataFinal:
        filtro = MetasVendas.dt_movimento.between(dataInicial, dataFinal)
        vendas = vendas.filter(filtro).first()
    else:
        vendas = vendas.filter(MetasVendas.dt_movimento == dataInicial).first()

    return vendas.total if vendas else 0.0


# VERIFICADO
def getQtdadeNotas(dataInicial, dataFinal=None):
    qtdNotas = MetasVendas.query
    if dataFinal:
        filtroPeriodo = MetasVendas.dt_movimento.between(dataInicial, dataFinal)
        qtdNotas = qtdNotas.filter(filtroPeriodo)     
    else:
        qtdNotas = qtdNotas.filter(MetasVendas.dt_movimento == dataInicial)
    qtdNotas = qtdNotas.count()
    
    return qtdNotas


def getVendasVendedores(dataInicial, dataFinal, tipo=None):
    query_total = (db.func.sum(MetasVendas.val_venda) + db.func.sum(MetasVendas.val_devolucao)).label('total')
    vendas_total = db.session.query(MetasVendas.id_vendedor, Vendedor.nome, query_total)
    
    filter_periodo = (MetasVendas.dt_movimento.between(dataInicial, dataFinal))
    vendas_total = vendas_total.filter(filter_periodo)
    vendas_total = vendas_total.filter(Vendedor.id_cli_for == MetasVendas.id_vendedor)

    if(tipo == 'E'):
        vendas_total = vendas_total.filter(Vendedor.vendedor_externo == 'T')
    if(tipo == 'I'):
        vendas_total = vendas_total.filter(Vendedor.vendedor_externo == 'F')
    vendas_total = vendas_total.group_by(MetasVendas.id_vendedor, Vendedor.nome)

    return vendas_total


# VERIFICADO
def getValLucroPeriodo(dataInicial, dataFinal=None):
    queryLucroTotal = (db.func.sum(MetasVendas.val_lucro)).label('valor')
    lucroPeriodo = db.session.query(queryLucroTotal)

    if dataFinal:
        lucroPeriodo = lucroPeriodo.filter(MetasVendas.dt_movimento.between(dataInicial, dataFinal))
    else:
        lucroPeriodo = lucroPeriodo.filter(MetasVendas.dt_movimento == dataInicial)
    lucroPeriodo = lucroPeriodo.first()

    if lucroPeriodo:
        lucroPeriodo = locale.currency(lucroPeriodo.valor, grouping=True)
    else:
        lucroPeriodo = 0.0
    
    return lucroPeriodo


# VERIFICADO
def getValMeta(numMes, ano=datetime.date.today().year):
    dtInicioMeta = '{}-{}-01'.format(ano, numMes)
    meta = db.session.query(Metas.descricao,
                            Metas.dataInicial,
                            Metas.dataFinal,
                            db.func.sum(MetasPrevisao.valorVenda).label('valTotalMeta'))
    meta = meta.filter(Metas.id == MetasPrevisao.idMeta)
    meta = meta.filter(Metas.dataInicial == dtInicioMeta)
    meta = meta.group_by(Metas.descricao,
                         Metas.dataInicial,
                         Metas.dataFinal).first()

    return meta


# VERIFICADO
def getTotalContasReceberPeriodo(dataInicial, dataFinal=None):
    total = db.session.query(db.func.sum(Receber.valTitulo).label('valor'))
    if dataFinal:
        filtro = Receber.dtVencimento.between(dataInicial, dataFinal)
        total = total.filter(filtro)
    else:
        total = total.filter(Receber.dtVencimento == dataInicial)
    total = total.first()

    return total.valor if total else 0.0


# VERIFICADO
def getTotalContasPagarPeriodo(dataInicial, dataFinal=None):
    total = db.session.query(db.func.sum(Pagar.valTitulo).label('valor'))
    if dataFinal:
        filtro = Pagar.dtVencimento.between(dataInicial, dataFinal)
        total = total.filter(filtro)
    else:
        total = total.filter(Pagar.dtVencimento == dataInicial)
    total = total.first()

    return total.valor if total else 0.0


def getProdutosPorQtdSaida(dataInicial, dataFinal=None, limit=None):
    queryCount = db.func.count(MetasVendas.id_produto).label('qtdade')
    produtos = db.session.query(MetasVendas.id_produto, Produto.descricao, queryCount)
    produtos = produtos.filter(Produto.id_subproduto == MetasVendas.id_produto)

    if dataFinal:
        filtro = MetasVendas.dt_movimento.between(dataInicial, dataFinal)
        produtos = produtos.filter(filtro)
    else:
        produtos = produtos.filter(MetasVendas.dt_movimento == dataInicial)
    produtos = produtos.group_by(MetasVendas.id_produto, Produto.descricao)
    produtos = produtos.order_by(db.desc(queryCount))

    if limit:
        produtos = produtos.limit(limit)

    return produtos


def getTotalCompraClientes(dataInicial, dataFinal=None, limit=None, convertToList=False):
    queryCount = db.func.sum(Estoque.valTotalLiq).label('total')
    clientes = db.session.query(Notas.idCliFor, Vendedor.nome, queryCount)
    
    clientes = clientes.filter(Notas.idEmpresa == Estoque.idEmpresa)
    clientes = clientes.filter(Notas.idPlanilha == Estoque.idPlanilha)
    clientes = clientes.filter(Notas.idCliFor == Vendedor.id_cli_for)
    clientes = clientes.filter(Notas.idCliFor != 242)
    clientes = clientes.filter(Notas.tipoNota == 'S')
    clientes = clientes.filter(Vendedor.tipo_cadastro == 'C')
    clientes = clientes.filter(Estoque.idOperacao.in_([1001, 29, 30, 31, 32]))

    if dataFinal:
        filtro = Notas.dtMovimento.between(dataInicial, dataFinal)
        clientes = clientes.filter(filtro)
    else:
        clientes = clientes.filter(Notas.dtMovimento == dataInicial)   
    
    clientes = clientes.group_by(Notas.idCliFor, Vendedor.nome)
    clientes = clientes.order_by(db.desc(queryCount))

    if limit:
        clientes = clientes.limit(limit)
    
    if convertToList:
        lista = []
        for cliente in clientes:
            data = {
                'idCliFor': cliente.idCliFor,
                'nome': cliente.nome,
                'total': locale.currency(cliente.total, grouping=True)
            }
            lista.append(data)
        clientes = lista
    
    return clientes


# VERIFICADO
def getProdutosEstoqueBaixo(tipoGiro=None, somenteZerados=False):
    produtos = db.session.query(SaldoProduto.id_subproduto)

    produtos = produtos.filter(SaldoProduto.id_produto == Sugestao.idProduto)
    produtos = produtos.filter(SaldoProduto.id_subproduto == Sugestao.idSubProduto)
    produtos = produtos.filter(SaldoProduto.qtd_atual < Sugestao.qtdMinima)
    
    if tipoGiro:
        produtos = produtos.filter(Sugestao.tipoGiro == tipoGiro)
    if somenteZerados:
        produtos = produtos.filter(SaldoProduto.qtd_atual == 0)
    
    return produtos


def getTotalVendasDoAnoPorMes(ano):
    # Define as colunas que vao ser retornadas na consulta em StokyMetasView
    query_total = (db.func.sum(MetasVendas.val_venda) + db.func.sum(MetasVendas.val_devolucao)).label('valor')
    vendasAno = db.session.query(query_total)
    
    # Define os filtros da consulta
    inicioAno = datetime.date(ano, 1, 1)
    finalAno = datetime.date(ano, 12, 31)
    filtro = MetasVendas.dt_movimento.between(inicioAno, finalAno)
    vendasAno = vendasAno.filter(filtro)
    vendasAno = vendasAno.group_by(db.func.month(MetasVendas.dt_movimento))

    listaVendasAno = []
    for mes in vendasAno:
        listaVendasAno.append(mes.valor)
    
    if len(listaVendasAno) < 12:
        count = 0
        mesesFaltando = 12 - len(listaVendasAno)
        while count < mesesFaltando:
            listaVendasAno.append(0.0)
            count += 1

    return listaVendasAno
