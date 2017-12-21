from app.application import db


class EstoqueAnalitico(db.Model):
    """
    Representa a tabela ESTOQUE_ANALITICO do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'ESTOQUE_ANALITICO'

    idPlanilha = db.Column('IDPLANILHA', db.Integer, primary_key=True)
    idEmpresa = db.Column('IDEMPRESA', db.Integer, primary_key=True)
    numSequencia = db.Column('NUMSEQUENCIA', db.Integer, primary_key=True)

    idVendedor = db.Column('IDVENDEDOR', db.ForeignKey('CLIENTE_FORNECEDOR.IDCLIFOR'))
    idProduto = db.Column('IDPRODUTO', db.ForeignKey('PRODUTOS_VIEW.IDPRODUTO'))
    idSubProduto = db.Column('IDSUBPRODUTO', db.ForeignKey('PRODUTOS_VIEW.IDSUBPRODUTO'))
    qtdProduto = db.Column('QTDPRODUTO', db.Numeric(12,3))
    valTotalLiq = db.Column('VALTOTLIQUIDO', db.Numeric(15,6))
    valTotalBruto = db.Column('VALTOTBRUTO', db.Numeric(15,6))
    dtMovimento = db.Column('DTMOVIMENTO', db.Date())
    idOperacao = db.Column('IDOPERACAO', db.Integer)

    join_produtos = "and_(ViewProduto.id_produto == EstoqueAnalitico.idProduto,\
                          ViewProduto.id_subproduto == EstoqueAnalitico.idSubProduto)"
    produto = db.relationship('ViewProduto', primaryjoin=join_produtos)
    vendedor = db.relationship('ClienteFornecedor')

