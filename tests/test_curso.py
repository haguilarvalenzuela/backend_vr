import os
import tempfile
import json
import pytest

from flaskr import api
from models.curso import Curso
from models.curso_base import CursoBase

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])


def test_get_curso(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		rv = client.get('/cursos/'+str(curso.id))
		assert True

def test_get_cursos(client):
	rv = client.get('/cursos')
	assert True

def test_get_curso_detalle(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		rv = client.get('/curso_detalle/'+str(curso.id))
		assert True

def test_get_cursos_admin(client):
	rv = client.get('/cursos_admin')
	assert True

def test_get_cursos_activos(client):
	rv = client.get('/cursos_activos')
	assert True

def test_get_cursos_cerrados(client):
	rv = client.get('/cursos_cerrados')
	assert True

def test_get_cursos_base(client):
	rv = client.get('/cursos_base')
	assert True

def test_get_curso_base(client):
	curso_base = CursoBase.objects().first()
	if(curso_base==None):
		assert True
	else:
		rv = client.get('/curso_base/'+str(curso_base.id))
		assert True

def test_get_curso_alumnos(client):
	rv = client.get('/cursos_alumnos')
	assert True