import os
import logging
from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import sta.modulos.ingesta.aplicacion
    import sta.modulos.imagenes.aplicacion


def importar_modelos_alchemy():
    import sta.modulos.ingesta.infraestructura.dto
    import sta.modulos.imagenes.infraestructura.dto


def comenzar_consumidor(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import sta.modulos.ingesta.infraestructura.consumidores as ingestas
    import sta.modulos.imagenes.infraestructura.consumidores as imagenes

    # Suscripción a eventos
    threading.Thread(target=imagenes.suscribirse_a_evento_ingesta_creada, args=(app,)).start()
    threading.Thread(target=imagenes.suscribirse_a_evento_ingesta_revertida, args=(app,)).start()

    # Suscripción a comandos
    threading.Thread(target=ingestas.suscribirse_a_comando_crear_ingesta, args=(app,)).start()
    threading.Thread(target=ingestas.suscribirse_a_comando_eliminar_ingesta, args=(app,)).start()
    threading.Thread(target=ingestas.suscribirse_a_comando_revertir_ingesta, args=(app,)).start()

DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="127.0.0.1")
DB_PORT = os.getenv('DB_PORT', default="3306")
DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="adminadmin")
DB_NAME = os.getenv('DB_NAME_STA', default="pruebas")


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from sta.config.db import init_db
    init_db(app)

    from sta.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    # Configurar el logger de SQLAlchemy
    #logging.basicConfig()
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    # Importa Blueprints
    from . import ingesta

    # Registro de Blueprints  
    app.register_blueprint(ingesta.bp)

    @app.route("/ingesta/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/ingesta/health")
    def health():
        return {"status": "up"}

    return app
