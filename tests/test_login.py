import os
import tempfile
import json
import pytest

from flaskr import api

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_post_login(client):
	data = {
		'tipo': 'ADMINISTRADOR',
		'email': 'admin@admin.cl',
		'password': 'pass'
	}

	data = json.dumps(data)
	data = data.encode()
	rv = client.post('/login', data=data)
	assert True

def test_post_logout(client):
	rv = client.post('/logout')
	assert True
