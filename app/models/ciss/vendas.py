from app.application import db


class Metas(db.Model):
    """
    Representa a tabela METAS do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'METAS'

    id = db.Column('IDMETA', db.Integer, primary_key=True)
    descricao = db.Column('DESCRMETA', db.String(60))
    dataInicial = db.Column('DTINICIAL', db.Date())
    dataFinal = db.Column('DTFINAL', db.Date())


class MetasPrevisao(db.Model):
    """
    Representa a tabela METAS_PREVISAO do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'METAS_PREVISAO'

    idMeta = db.Column('IDMETA', db.ForeignKey('METAS.IDMETA'), primary_key=True)
    idSeq = db.Column('NUMSEQUENCIA', db.Integer, primary_key=True)
    valorVenda = db.Column('METAVLRVENDA', db.Numeric(10, 2))

    meta = db.relationship("Metas", backref=db.backref('metasPrevisao'))