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


    from apptax.taxonomie.routesbibtaxons import adresses
    app.register_blueprint(adresses, url_prefix='/bibtaxons')

    from apptax.taxonomie.routestaxref import adresses
    app.register_blueprint(adresses, url_prefix='/taxref')

    from apptax.taxonomie.routesbibattributs import adresses
    app.register_blueprint(adresses, url_prefix='/bibattributs')

    return app


if __name__ == '__main__':
    init_app().run(debug=True)
