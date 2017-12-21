from app.application import db


class Empresa(db.Model):
    """
    Representa a tabela EMPRESA do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'EMPRESA'

    cli_id = db.Column('IDEMPRESA', db.Integer, primary_key=True)
    descricao = db.Column('NOMEFANTASIA', db.String(120))


class ClienteFornecedor(db.Model):
    """
    Representa a tabela CLIENTE_FORNECEDOR do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'CLIENTE_FORNECEDOR'

    id_cli_for = db.Column('IDCLIFOR', db.Integer, primary_key=True)
    nome = db.Column('NOME', db.String(80), nullable=False)
    uf_cli_for = db.Column('UFCLIFOR', db.String(2))

    c_tipo_cadastro = "tipo_cadastro == 'C'"
    c_tipo_cadastro = c_tipo_cadastro + "or tipo_cadastro == 'C'"
    c_tipo_cadastro = c_tipo_cadastro + "or tipo_cadastro == 'A'"
    c_tipo_cadastro = c_tipo_cadastro + "or tipo_cadastro == 'u'"
    c_tipo_cadastro = c_tipo_cadastro + "or tipo_cadastro == 'F'"
    c_tipo_cadastro = c_tipo_cadastro + "or tipo_cadastro == 'V'"
    tipo_cadastro = db.Column('TIPOCADASTRO', 
                              db.String(1),
                              db.CheckConstraint(c_tipo_cadastro))
    
    c_vendedor_externo = "vendedor_externo=='T' or vendedor_externo=='F'"
    vendedor_externo = db.Column('FLAGVENDEDOREXTERNO', db.String(1),
                                 db.CheckConstraint(c_vendedor_externo))
    
    c_inativo = "inativo=='T' or inativo=='F'"
    inativo = db.Column('FLAGINATIVO', db.String(1),
                        db.CheckConstraint(c_inativo))


class Marca(db.Model):
    """
    Representa a tabela MARCA do Ciss
    """

    __bind_key__ = 'ciss'
    __tablename__ = 'MARCA'

    marca_id = db.Column('IDMARCAFABRICANTE', db.Integer, primary_key=True)
    descricao = db.Column('DESCRICAO', db.String(100))
