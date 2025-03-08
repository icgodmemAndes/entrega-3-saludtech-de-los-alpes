import os
import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import anonimizador.modulos.anonimizado.aplicacion


def importar_modelos_alchemy():
    import anonimizador.modulos.anonimizado.infraestructura.dto


def comenzar_consumidor(app):
    import threading
    import anonimizador.modulos.anonimizado.infraestructura.consumidores as anonimizados
    import anonimizador.modulos.anonimizado.infraestructura.compensacion.compensacion_from_etiquetado as compensacion

    # Suscripción a eventos
    threading.Thread(target=anonimizados.suscribirse_a_eventos, args=(app,)).start()
    # Suscripción a comandos
    threading.Thread(target=compensacion.suscribirse_a_comando_compensacion, args=(app,)).start()
    # ...


DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="127.0.0.1")
DB_PORT = os.getenv('DB_PORT', default="3306")
DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="adminadmin")
DB_NAME = os.getenv('DB_NAME_ANONIMIZADOR', default="pruebas")


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.config['TESTING'] = configuracion.get('TESTING')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = '9d58f98f-3ae8-4149-a19f-3a8c2012e32c'

    # Inicializa la DB
    from anonimizador.config.db import init_db
    init_db(app)

    from anonimizador.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    # Configurar el logger de SQLAlchemy
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    @app.route("/anonimizador/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/anonimizador/health")
    def health():
        return {"status": "up"}

    return app
