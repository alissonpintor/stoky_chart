from app.application import db
from app.models.ciss.cadastros import Empresa, Marca, ClienteFornecedor


class ViewProduto(db.Model):
    """
    Representa a View PRODUTOS_VIEW do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'PRODUTOS_VIEW'

    id_produto = db.Column('IDPRODUTO', db.Integer, primary_key=True)
    id_subproduto = db.Column('IDSUBPRODUTO', db.Integer, primary_key=True)
    descricao = db.Column('DESCRICAOPRODUTO', db.String(100))
    fabricante = db.Column('FABRICANTE', db.String(50))
    flag_inativo = db.Column('FLAGINATIVO', db.String(1), 
                             db.CheckConstraint("flag_inativo=='T' or flag_inativo=='F'"))


class ViewSaldoProduto(db.Model):
    """
    Representa a View PRODUTOS_SALDOS_VIEW do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'PRODUTOS_SALDOS_VIEW'
    id_produto = db.Column('IDPRODUTO', db.ForeignKey('PRODUTOS_VIEW.IDPRODUTO'), primary_key=True)
    id_subproduto = db.Column('IDSUBPRODUTO', db.ForeignKey('PRODUTOS_VIEW.IDSUBPRODUTO'), primary_key=True)
    id_empresa = db.Column('IDEMPRESA', db.Integer, primary_key=True)
    qtd_atual = db.Column('QTDATUALESTOQUE', db.Numeric(10,2))
    qtd_disponivel = db.Column('QTDDISPONIVEL', db.Numeric(10,2))
    qtd_reserva = db.Column('QTDSALDORESERVA', db.Numeric(10,2))

    # Relacionamentos da View
    v_produto = db.relationship('ViewProduto',
                                primaryjoin="and_(ViewSaldoProduto.id_produto == ViewProduto.id_produto, "
                                            "ViewSaldoProduto.id_subproduto == ViewProduto.id_subproduto)",
                                backref=db.backref('v_produto_saldo'))


class StokyMetasView(db.Model):
    """
    Representa a View STOKY_METAS do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'STOKY_METAS'

    id_planilha = db.Column('IDPLANILHA', db.Integer, primary_key=True)
    id_empresa = db.Column('IDEMPRESA', db.Integer, db.ForeignKey('EMPRESA.IDEMPRESA'), primary_key=True)
    id_sequencia = db.Column('NUMSEQUENCIA', db.Integer, primary_key=True)
    id_vendedor = db.Column('IDVENDEDOR', db.Integer, db.ForeignKey('CLIENTE_FORNECEDOR.IDCLIFOR'), nullable=False)
    dt_movimento = db.Column('DTMOVIMENTO', db.Date())
    id_produto = db.Column('IDSUBPRODUTO', db.Integer, db.ForeignKey('PRODUTOS_VIEW.IDSUBPRODUTO'), nullable=False)
    id_marca = db.Column('IDMARCAFABRICANTE', db.Integer, db.ForeignKey('MARCA.IDMARCAFABRICANTE'))
    val_venda = db.Column('VENDA', db.Numeric(10, 2))
    val_devolucao = db.Column('DEVOLUCAO', db.Numeric(10, 2))
    val_lucro = db.Column('LUCRO', db.Numeric(10, 2))

    # Relacionamentos da View
    vendedor = db.relationship("ClienteFornecedor")
    produto = db.relationship('ViewProduto')
    marca = db.relationship('Marca')


class ViewContasReceber(db.Model):
    """
    Representa a View CONTAS_RECEBER_SALDOS_VIEW do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'CONTAS_RECEBER_SALDOS_VIEW'

    idEmpresa = db.Column('IDEMPRESA', db.Integer, primary_key=True)
    idCliFor = db.Column('IDCLIFOR', db.ForeignKey('CLIENTE_FORNECEDOR.IDCLIFOR'), primary_key=True)
    idTitulo = db.Column('IDTITULO', db.Integer, primary_key=True)
    serieNota = db.Column('SERIENOTA', db.String(3), primary_key=True)
    digTitulo = db.Column('DIGITOTITULO', db.String(2), primary_key=True)
    valTitulo = db.Column('VALTITULO', db.Numeric(14,2))
    valLiqTitulo = db.Column('VALLIQUIDOTITULO', db.Numeric(14,2))
    valPagoTitulo = db.Column('SUMVALPAGAMENTOTITULO', db.Numeric(14,2))
    dtMovimento = db.Column('DTMOVIMENTO', db.Date())
    dtVencimento = db.Column('DTVENCIMENTO', db.Date())
    jurosMora = db.Column('SUMVALJUROSMORA', db.Numeric(14,2))
    jurosCobrado = db.Column('SUMVALJUROSCOBRADO', db.Numeric(14,2))

    cliente = db.relationship('ClienteFornecedor')


class ViewContasPagar(db.Model):
    """
    Representa a View CONTAS_PAGAR_SALDOS_VIEW do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'CONTAS_PAGAR_SALDOS_VIEW'

    idEmpresa = db.Column('IDEMPRESA', db.Integer, primary_key=True)
    idCliFor = db.Column('IDCLIFOR', db.ForeignKey('CLIENTE_FORNECEDOR.IDCLIFOR'), primary_key=True)
    idTitulo = db.Column('IDTITULO', db.Integer, primary_key=True)
    serieNota = db.Column('SERIENOTA', db.String(3), primary_key=True)
    digTitulo = db.Column('DIGITOTITULO', db.String(2), primary_key=True)
    valTitulo = db.Column('VALTITULO', db.Numeric(14,2))
    valLiqTitulo = db.Column('VALLIQUIDOTITULO', db.Numeric(14,2))
    valPagoTitulo = db.Column('SUMVALPAGAMENTOTITULO', db.Numeric(14,2))
    dtMovimento = db.Column('DTMOVIMENTO', db.Date())
    dtVencimento = db.Column('DTVENCIMENTO', db.Date())
    jurosMora = db.Column('SUMVALJUROSMORA', db.Numeric(14,2))
    jurosCobrado = db.Column('SUMVALJUROSCOBRADO', db.Numeric(14,2))

    fornecedor = db.relationship('ClienteFornecedor')