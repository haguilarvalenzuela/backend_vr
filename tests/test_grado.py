import os
import tempfile
import json
import pytest

from flaskr import api
from models.grado import Grado
from models.institucion import Institucion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_grado(client):
	rv = client.get('/grados')
	assert True

def test_get_grado_id(client):
	grado = Grado.objects().first()
	if(grado==None):
		assert True
	else:
		rv = client.get('/grados/'+str(grado.id))
		assert True

def test_get_grados_detalle(client):
	rv = client.get('/grados_detalle')
	assert True

def test_post_grado(client):
	institucion = Institucion.objects().first()
	
	if(institucion==None):
		assert True
	else:
		data = {
			"institucion": str(institucion.id),
			"nivel": 1,
			"identificador": 'A',
			"activo": True
		}
		data = json.dumps(data)
		data = data.encode(data)
		rv = client.post('/grados', data=data)
		assert True

def test_delete_grado_id(client):
	grado = Grado.objects().first()
	if(grado==None):
		assert True
	else:
		rv = client.delete('/grados/'+str(grado.id))
		assert True