from flask import Flask, Blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from flask_login import LoginManager
from db import db
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp)


def init_modules(app, api):
    from resources import curso
    from resources import alumno
    from resources import institucion
    from resources import asignatura
    from resources import profesor
    from resources import evaluacion
    from resources import inscripcion
    from resources import administrador
    from resources import portal
    from resources import seccion
    from resources import grado
    from resources import login

    curso.init_module(api)
    alumno.init_module(api)
    institucion.init_module(api)
    asignatura.init_module(api)
    profesor.init_module(api)
    evaluacion.init_module(api)
    inscripcion.init_module(api)
    administrador.init_module(api)
    portal.init_module(api)
    seccion.init_module(api)
    grado.init_module(api)
    login.init_module(api)

init_modules(app, api)

if __name__ == '__main__':
    app.run(debug=True)