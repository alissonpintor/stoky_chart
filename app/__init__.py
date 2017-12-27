from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES


assets = Environment()
db = SQLAlchemy()
loginManager = LoginManager()
imageSet = UploadSet('photos', IMAGES)
