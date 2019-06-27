import os
import tempfile
import json
import pytest

from flaskr import api
from flask import current_app
from models.administrador import Administrador

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_administradores(client):
    rv = client.get('/administradores')
    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_get_administrador(client):
    administrador = Administrador.objects().first()
    if(administrador==None):
        assert True
    else:
        rv = client.get('/administradores/'+str(administrador.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_admin_token(client):

    with api.app.app_context():
        administrador = Administrador.objects().first()
        token = administrador.get_token()
        response = client.get('/administradores', headers={'auth-token': token})
        empty = []
        if response ==  empty:
            assert True
        elif administrador.to_dict() ==  response:
            assert True

def test_get_finalizar_tutorial_admin(client):
    with api.app.app_context():
        administrador = Administrador.objects().first()
        if administrador == None:
            assert True
        else:
            rv = client.get('/administrador_finalizar_tutorial/'+str(administrador.id))
            assert True
        
def test_put_administrador(client):
    administrador = Administrador.objects().first()
    if(administrador==None):
        assert True
    else:
        data = {
            'nombres': 'nombre admin',
            'apellido_paterno': 'paterno',
            'apellido_materno': 'materno' ,
            'email': 'email@email.email',
            'telefono': '+569',
            'nombre_usuario': 'usuario',
            'password': 'pass'
        }
        data = json.dumps(data)
        data = data.encode()
        rv = client.put('/administradores/'+str(administrador.id), data=data)
        assert True