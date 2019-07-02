import os
import tempfile
import json
import pytest

from flaskr import api
from models.inscripcion import Inscripcion
from models.alumno import Alumno
from models.curso import Curso
from models.historial import Historial

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_inscripcion_item(client):
	inscripcion = Inscripcion.objects().first()
	if inscripcion == None:
		assert True
	else:
		rv = client.get('/inscripciones/'+str(inscripcion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_delete_inscripcion_item(client):
	inscripcion = Inscripcion.objects().first()
	if inscripcion == None:
		assert True
	else:
		rv = client.delete('/inscripciones/'+str(inscripcion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_put_inscripcion_item(client):
	inscripcion = Inscripcion.objects().first()
	if inscripcion == None:
		assert True
	else:
		data = {
			'estado': 'estado',
			'mensaje': 'mensaje'
		}

		rv = client.put('/inscripciones/'+str(inscripcion.id), data=data)
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_post_inscripciones_aceptar(client):
	recurso = Curso.objects().first()
	if recurso == None:
		assert True
	else:
		rv = client.post('/aceptar/inscripciones/recurso/'+str(recurso.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_inscripcion_recurso(client):
	recurso = Curso.objects().first()
	if recurso == None:
		assert True
	else:
		rv = client.get('/inscripciones/recurso/'+str(recurso.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_post_inscripcion_recurso(client):
	recurso = Curso.objects().first()
	alumno = Alumno.objects().first()
	if recurso == None or alumno == None:
		assert True
	else:
		data = {
			'id_alumno': alumno.id
		}
		data = json.dumps(data)
		data = data.encode()
		rv = client.post('/inscripciones/recurso/'+str(recurso.id), data=data)
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_inscripciones_alumno(client):
	inscripcion = Inscripcion.objects().first()
	if inscripcion == None:
		assert True
	else:
		rv = client.get('/inscripciones/alumno/'+str(inscripcion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_inscripciones(client):
	rv = client.get('/inscripciones')
	if rv._status_code == 200:
		assert True
	else:
		assert False