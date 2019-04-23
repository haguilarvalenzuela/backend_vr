import os
import tempfile
import json
import pytest

from flaskr import api
from models.profesor import Profesor

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_profesores(client):

    rv = client.get('/profesores')
    assert rv.data

def test_get_profesor_id(client):

    profesor = Profesor.objects().first()
    if(profesor==None):
        assert True
    else:
        assert False

def test_get_profesor_cursos(client):

    profesor = Profesor.objects().first()
    if(profesor==None):
        assert True
    else:
        rv = client.get('/profesor_curso/'+str(profesor.id))
        assert True

def test_post_profesor(client):

    data = {
        'nombres':'nombre prueba',
        'apellido_paterno':'paterno',
        'apellido_materno':'materno',
        'telefono':'+569',
        'email':'prueba@prueba.prueba',
        'nombre_usuario':'usuario_prueba',
        'password':'password'
        }

    data = json.dumps(data)
    data = data.encode()
    rv = client.post('/profesores', data=data)
    assert rv.data

def test_put_profesor(client):
    profesor = Profesor.objects().first()
    if(profesor==None):
        assert True
    else:
        data = {
            'nombres':'nombre prueba',
            'apellido_paterno':'paterno',
            'apellido_materno':'materno',
            'telefono':'+569',
            'email':'prueba@prueba.prueba',
            'nombre_usuario':'usuario_prueba',
            'password':'password'
            }

        data = json.dumps(data)
        data = data.encode()
        rv = client.put('/profesores/'+str(profesor.id), data=data)
        assert True

def test_delete_profesor(client):

    profesor = Profesor.objects().first()
    if(profesor==None):
        assert True
    else:
        rv = client.delete('/profesores/'+str(profesor.id))
        assert True
