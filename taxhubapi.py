from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app_globals = {}

def init_app():
    if app_globals.get('app', False):
        app= app_globals['app']
    else :
        app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)
    app_globals['app'] = app


    from apptax.bibtaxons.routes import adresses
    app.register_blueprint(adresses, url_prefix='/bib_taxons')

    from apptax.taxref.routes import adresses
    app.register_blueprint(adresses, url_prefix='/taxref')


    return app


if __name__ == '__main__':
    init_app().run(debug=True)
