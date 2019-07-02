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
	if rv._status_code == 200:
		assert True
	else:
		assert False

def test_post_logout(client):
	rv = client.post('/logout')
	if rv._status_code == 200:
		assert True
	else:
		assert False

def test_post_login_app(client):
	data = {
		'tipo': 'ADMINISTRADOR',
		'email': 'admin@admin.cl',
		'password': 'pass'
	}

	data = json.dumps(data)
	data = data.encode()
	rv = client.post('/login/app/',data=data)
	if rv._status_code == 200 or rv._status_code == 403:
		assert True
	else:
		assert False
