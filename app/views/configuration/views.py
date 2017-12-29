from flask import Blueprint, render_template, current_app
from flask_login import login_required
from flask_uploads import configure_uploads
from app import db, imageSet

# Import dos Forms da View
from app.views.configuration.forms import ConfigForm

# Import das Models usadas pela View
from app.models.appConfig import Config


configuration = Blueprint('configuration', __name__)


@configuration.route('/', methods=['GET', 'POST'])
def index():
    config = Config.query.filter_by(id=1).first()
    form = ConfigForm()

    if config and not form.baseURL.data:
        form.configId.data = config.id
        form.baseURL.data = config.baseUrl
    
    if form.validate_on_submit():
        import os
        config.baseUrl = form.baseURL.data
        
        uploadURL = os.path.join(form.baseURL.data, 'uploads')
        current_app.config.update(
            UPLOADS_DEFAULT_URL=uploadURL
        )
        configure_uploads(current_app, (imageSet, ))

        db.session.add(config)
        db.session.commit()

    content = {
        'title': 'Configurações do Sistema',
        'form': form
    }
    return render_template('configurations/main.html', **content)
