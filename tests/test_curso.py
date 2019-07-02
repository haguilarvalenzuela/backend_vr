import os
import tempfile
import json
import pytest

from flaskr import api
from models.grado import Grado
from models.institucion import Institucion
from models.profesor import Profesor


@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

#/cursos/id
def test_get_curso_item(client):
    curso = Grado.objects().first()
    if curso == None:
        assert True
    else:
        rv = client.get('/cursos/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_delete_curso_item(client):
    curso = Grado.objects().first()
    if curso == None:
        assert True
    else:
        rv = client.delete('/cursos/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_cursos(client):
    rv = client.get('/cursos')
    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_post_cursos(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        data = {
            'profesor': str(profesor.id),
            'nivel': '1',
            'identificador': 'A'
        }
        data = json.dumps(data)
        data = data.encode()
        rv = client.post('/cursos', data=data)
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_cursos_profesor(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/cursos/profesor/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_cursos_detalle(client):
    rv = client.get('/cursos/detalle')
    if rv._status_code == 200:
        assert True
    else:
        assert False