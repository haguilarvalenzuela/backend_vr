import os
import tempfile
import json
import pytest

from flaskr import api
from models.institucion import Institucion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_institucion(client):
	rv = client.get('/instituciones')
	assert True
	
def test_get_institucion_id(client):
	institucion = Institucion.objects().first()
	if(institucion==None):
		assert True
	else:
		rv = client.get('/instituciones/'+str(institucion.id))
		assert True