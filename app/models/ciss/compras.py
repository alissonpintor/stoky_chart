from app.application import db


class Notas(db.Model):
    """
    Representa a tabela NOTAS do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'NOTAS'

    idPlanilha = db.Column('IDPLANILHA', db.Integer, primary_key=True)
    idEmpresa = db.Column('IDEMPRESA', db.Integer, primary_key=True)

    numNota = db.Column('NUMNOTA', db.Integer)
    idCliFor = db.Column('IDCLIFOR', db.ForeignKey('CLIENTE_FORNECEDOR.IDCLIFOR'))
    dtMovimento = db.Column('DTMOVIMENTO', db.Date())
    tipoNota = db.Column('TIPONOTAFISCAL', db.String(1))

    db.CheckConstraint("tipoNota=='E' or tipoNota='S'")
    cliente = db.relationship('ClienteFornecedor')


class SugestaoCompra(db.Model):
    """
    Representa a tabela PRODUTO_COMPRAS do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'PRODUTO_COMPRAS'

    idEmpresa = db.Column('IDEMPRESA', db.Integer, primary_key=True)
    idProduto = db.Column('IDPRODUTO', db.ForeignKey('PRODUTOS_VIEW.IDPRODUTO'), primary_key=True)
    idSubProduto = db.Column('IDSUBPRODUTO', db.ForeignKey('PRODUTOS_VIEW.IDSUBPRODUTO'), primary_key=True)

    qtdMinima = db.Column('QTDESTMINIMO', db.Integer)
    qtdMaxima = db.Column('QTDESTMAXIMO', db.Integer)
    tipoGiro = db.Column('TIPOGIRO', db.String(1))