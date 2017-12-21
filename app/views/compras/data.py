# import da aplicação
from app.application import db

# Import das Models da Aplicação
from app.models.ciss.views import ViewProduto as Produto
from app.models.ciss.views import ViewSaldoProduto as SaldoProduto
from app.models.ciss.compras import Notas, SugestaoCompra as Sugestao


def getProdutosEstoqueBaixo(tipoGiro=None, somenteZerados=False):
    produtos = db.session.query(SaldoProduto.id_subproduto, 
                                Produto.descricao,
                                Produto.fabricante,
                                SaldoProduto.qtd_atual,
                                Sugestao.qtdMinima)

    produtos = produtos.filter(SaldoProduto.id_produto == Sugestao.idProduto)
    produtos = produtos.filter(SaldoProduto.id_subproduto == Sugestao.idSubProduto)
    produtos = produtos.filter(SaldoProduto.id_produto == Produto.id_produto)
    produtos = produtos.filter(SaldoProduto.id_subproduto == Produto.id_subproduto)
    produtos = produtos.filter(SaldoProduto.qtd_atual < Sugestao.qtdMinima)
    
    if tipoGiro:
        produtos = produtos.filter(Sugestao.tipoGiro == tipoGiro)
    if somenteZerados:
        produtos = produtos.filter(SaldoProduto.qtd_atual == 0)
    
    produtos = produtos.order_by(Produto.fabricante, Produto.descricao)

    produtosToJson = {}
    for produto in produtos:
        fabricante = produto.fabricante.lower()
        
        if not fabricante in produtosToJson:            
            produtosToJson[ fabricante ] = []
        
        produtosToJson[ fabricante ].append({
            'id_subproduto': produto.id_subproduto,
            'descricao': produto.descricao.title(),
            'fabricante': produto.fabricante.title(),
            'qtd_atual': str(produto.qtd_atual),
            'qtdMinima': str(produto.qtdMinima),
        })
    
    return produtos, produtosToJson


def getMarcasEstoqueBaixo(tipoGiro=None, somenteZerados=False):
    queryCount = db.func.count(SaldoProduto.id_subproduto).label('total')
    marcasTotal = db.session.query(Produto.fabricante, queryCount)

    marcasTotal = marcasTotal.filter(SaldoProduto.id_produto == Sugestao.idProduto)
    marcasTotal = marcasTotal.filter(SaldoProduto.id_subproduto == Sugestao.idSubProduto)
    marcasTotal = marcasTotal.filter(SaldoProduto.id_produto == Produto.id_produto)
    marcasTotal = marcasTotal.filter(SaldoProduto.id_subproduto == Produto.id_subproduto)
    marcasTotal = marcasTotal.filter(SaldoProduto.qtd_atual < Sugestao.qtdMinima)
    
    if tipoGiro:
        marcasTotal = marcasTotal.filter(Sugestao.tipoGiro == tipoGiro)
    marcasTotal = marcasTotal.group_by(Produto.fabricante)
    marcasTotal = marcasTotal.order_by(Produto.fabricante)

    resultadoMarcas = []
    for marca in marcasTotal:
        
        marcaZerados = marcasTotal.filter(SaldoProduto.qtd_atual == 0)
        marcaZerados = marcaZerados.filter(Produto.fabricante == marca.fabricante)
        marcaZerados = marcaZerados.first()
        
        if marcaZerados:
            resultadoMarcas.append({
                'fabricante': marca.fabricante,
                'total': marca.total,
                'zerados': marcaZerados.total
            })
        elif not somenteZerados:
            resultadoMarcas.append({
                'fabricante': marca.fabricante,
                'total': marca.total,
                'zerados': 0
            })
    
    return resultadoMarcas