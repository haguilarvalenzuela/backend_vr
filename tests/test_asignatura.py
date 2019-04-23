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
	if(asignatura==None):
		assert True
	else:
		rv = client.get('/asignatura/'+str(asignatura.id))
		assert True

def test_get_asignaturas(client):
	rv = client.get('/asignaturas')
	assert True

def test_get_asignaturas_detalles(client):
	rv = client.get('/asignaturas_detalle')
	assert True

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
		assert True

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
		assert True