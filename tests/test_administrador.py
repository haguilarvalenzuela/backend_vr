import os
import tempfile
import json
import pytest

from flaskr import api
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
	assert rv.data

def test_get_administrador(client):
    administrador = Administrador.objects().first()
    if(administrador==None):
        assert True
    else:
        rv = client.get('/administradores/'+str(administrador.id))
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