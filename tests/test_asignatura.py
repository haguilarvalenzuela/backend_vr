import os
import tempfile
import json
import pytest

from flaskr import api
from models.asignatura import Asignatura
from models.institucion import Institucion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_asignatura(client):
	asignatura = Asignatura.objects().first()
	if asignatura==None :
		assert True
	else:
		rv = client.get('/asignatura/'+str(asignatura.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_asignaturas(client):
	rv = client.get('/asignaturas')
	if rv._status_code == 200:		
		assert True
	else:
		assert False

def test_get_asignaturas_detalles(client):
	rv = client.get('/asignaturas/detalle')
	if rv._status_code == 200:
		assert True
	else:
		assert False

def test_post_asignatura(client):
	institucion = Institucion.objects().first()
	if(institucion==None):
		assert True
	else:
		data = {
			'nombre': 'nombre',
			'institucion': str(institucion.id)
		}
		data = json.dumps(data)
		data = data.encode()
		rv = client.post('/asignaturas', data=data)
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_put_asignatura(client):
	asignatura = Asignatura.objects().first()
	institucion = Institucion.objects().first()
	if(asignatura==None):
		assert True
	else:
		data = {
			'nombre': 'nombre',
			'institucion': str(institucion.id)
		}
		data = json.dumps(data)
		data = data.encode()
		rv = client.put('/asignaturas/'+str(asignatura.id), data=data)
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_delete_asignatura(client):
	asignatura = Asignatura.objects().first()
	if asignatura == None:
		assert True
	else:
		rv = client.delete('/asignaturas/'+str(asignatura.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_post_asignaturas(client):
	institucion = Institucion.objects().first()
	if institucion == None:
		assert True
	else:

		data = {
			'nombre': 'nombre',
					'institucion': str(institucion.id)
		}
		rv = client.post('/asignaturas', data=data)
		if rv._status_code == 200:
			assert True
		else:
			assert False
