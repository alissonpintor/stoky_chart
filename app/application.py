from app import assets, db
from app.bundles import css, js
from app.config import app_config

from flask import Flask
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

    assets.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    assets.register('css', css)
    assets.register('js', js)

    # Importa as Blueprints
    from app.views.index import bp
    from app.views.dashboard.views import dashboard
    from app.views.compras.views import compras

    # Registra as Blueprints
    app.register_blueprint(bp, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(compras, url_prefix='/compras')

    # Importa as Models
    from app.models import pessoas
    from app.models.ciss import cadastros, compras
    from app.models.ciss import vendas, estoques

    # Cria o Banco de Dados
    with app.app_context():
        db.create_all(bind=None)

    return app