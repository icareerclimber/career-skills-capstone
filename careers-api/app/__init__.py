from flask import Flask

app = Flask(__name__)

from app import routes

from app.models import bp as models_bp
app.register_blueprint(models_bp, url_prefix='/model')
