import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
from flaskr import api
from models.profesor import Profesor

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_profesor_item(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/profesores/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_delete_profesor_item(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.delete('/profesores/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_put_profesor_item(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        data = {
            'nombres': 'nombres',
            'apellido_paterno': 'apellido',
            'apellido_materno': 'apellido',
            'telefono': '999999',
            'email': 'email@email.cl',
            'nombre_usuario': 'usuario'
        }
        data = json.dumps(data)
        data = data.encode()
        rv = client.put('/profesores/'+str(profesor.id), data=data)
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_profesores(client):
    rv = client.get('/profesores')
    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_get_profesor_recursos(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/profesor/recursos/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_post_profesor_imagen(client):
    with api.app.app_context():

        directory_root = dirname(dirname(abspath(__file__)))
        path_img = os.path.join(str(directory_root),
                                "flaskr/uploads/categorias/default.jpg")

        with open(path_img, 'rb') as img_open:
            img = BytesIO(img_open.read())

            profesor = Profesor.objects().first()

            if profesor == None:
                assert True
            else:
                data = {
                    'imagen': (img, 'img.jpg')
                }
                rv = client.post('/profesor/imagen/'+str(profesor.id), content_type='multipart/form-data', data=data)
                print(rv._status_code)
                if rv._status_code == 200:
                    assert True
                else:
                    assert False

def test_get_profesor_imagen(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/profesor/imagen/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_profesor_imagen_default(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/profesor/imagen/default/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_post_profesor_token(client):
    with api.app.app_context():
        profesor = Profesor.objects().first()
        if profesor == None:
            assert True
        else:
            data = {
                'nombres': 'nombres',
                'apellido_paterno': 'apellido_paterno',
                'apellido_materno': 'apellido_materno',
                'telefono': 'telefono',
                'email': 'email',
                'nombre_usuario': 'usuario'
            }
            data = json.dumps(data)
            data = data.encode()
            token = profesor.get_token()
            rv = client.post('/profesores/token/'+token, data=data)
            if rv._status_code == 200:
                assert True
            else:
                assert False


def test_get_profesor_finalizar_tutorial(client):
    profesor = Profesor.objects().first()
    if profesor == None:
        assert True
    else:
        rv = client.get('/profesor/finalizar/tutorial/'+str(profesor.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False