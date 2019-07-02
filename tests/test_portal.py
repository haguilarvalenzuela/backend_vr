import os
import tempfile
import json
import pytest

from flaskr import api
from models.portal import Portal

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_portal(client):
	rv = client.get('/portales')
	if rv._status_code == 200:
		assert True
	else:
		assert False

def test_get_portal_id(client):
	portal = Portal.objects().first()
	if(portal==None):
		assert True
	else:
		rv = client.get('/portales/'+str(portal.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False
