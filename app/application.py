from app import assets, db, loginManager, imageSet
from app.bundles import css, js
from app.config import app_config

from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_uploads import configure_uploads


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

    assets.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    assets.register('css', css)
    assets.register('js', js)

    # Inicia o Login Manager
    loginManager.init_app(app)

    # imports do core
    from app.core.errorhandler import createErrorHandler
    createErrorHandler(app)

    # Configura o Flask-Uploads para upload de arquivos e fotos
    configure_uploads(app, (imageSet, ))

    # Importa as Blueprints
    from app.views.index import bp
    from app.views.account.views import account
    from app.views.dashboard.views import dashboard
    from app.views.compras.views import compras

    # Registra as Blueprints
    app.register_blueprint(bp, url_prefix='/')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(compras, url_prefix='/compras')

    # Import e Registro dos Custom Filters do Jinja
    from app.core.filters import regitryFilters
    regitryFilters(app)

    # Importa as Models
    from app.models import userAccess
    from app.models.ciss import cadastros, compras
    from app.models.ciss import vendas, estoques

    # Correção do erro de Conexão Perdida do SQLAlchemy
    from app.core.sqlalchemyerror import sqlalchemyErrorHandler
    
    # Cria o Banco de Dados
    with app.app_context():
        db.create_all(bind=None)
        sqlalchemyErrorHandler(db)
        
        # Cria o usuario admin se não existe
        if not userAccess.User.hasAdmin():
            userAccess.User.createAdmin()
    
    @app.route('/uploads/<path>/<filename>')
    def uploaded_file(path, filename):
        import os
        folder = os.path.join(app.config['UPLOAD_FOLDER'], path)
        return send_from_directory(folder, filename)

    return app
