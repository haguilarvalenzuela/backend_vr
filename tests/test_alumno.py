import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath

from flaskr import api
from models.alumno import Alumno
from models.curso import Curso
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

def test_get_alumno(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/alumnos/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_delete_alumno(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.delete('/alumnos/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_put_alumno(client):
    alumno = Alumno.objects().first()
    institucion = Institucion.objects().first()
    if alumno == None or institucion == None:
        assert True
    else:
        data = {
            'nombres': 'nombre prueba',
            'apellido_paterno': 'paterno',
            'apellido_materno': 'materno',
            'email': 'prueba@prueba.prueba',
            'telefono': '+560',
            'nombre_usuario': 'usuario_prueba',
            'password': 'asd',
            'matricula': 'matricula',
            'institucion': str(institucion.id)
        }
        data = json.dumps(data)
        data = data.encode()
        rv = client.put('/alumnos/'+str(alumno.id), data=data)
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_alumnos(client):
    rv = client.get('/alumnos')
    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_post_alumno(client):
    grado = Grado.objects().first()
    if grado == None:
        grado = 'None'
    else:
        grado = str(grado.id)
    data_personal = {
        'nombres': 'nombre prueba',
        'apellido_paterno': 'paterno',
        'apellido_materno': 'materno',
        'email': 'email@email.email',
        'telefono': '+569',
        'imagen': 'path/to/img',
        'grado': grado
    }

    data_academico = {
        'nombre_usuario': 'usuario_prueba',
        'password': 'asd',
        'matricula': 'matricula'
    }

    data = {
        'data_personal': data_personal,
        'data_academico': data_academico
    }

    data = json.dumps(data)
    data = data.encode()
    rv = client.post('/alumnos', data=data)

    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_get_alumno_recursos(client):
    curso = Curso.objects().first()
    if curso == None:
        assert True
    else:
        rv = client.get('/alumno/recursos/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False
        
def test_get_alumnos_recurso(client):
    curso = Curso.objects().first()
    if curso == None:
        assert True
    else:
        rv = client.get('/alumnos/recurso/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_post_alumno_recurso(client):
    curso = Curso.objects().first()
    alumno = Alumno.objects().first()

    if curso == None or alumno == None:
        assert True
    else:
        rv = client.post('/alumno/recurso/'+str(alumno.nombre_usuario)+'/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_delete_alumno_recurso(client):
    curso = Curso.objects().first()
    alumno = Alumno.objects().first()

    if curso == None or alumno == None:
        assert True
    else:
        rv = client.delete('/alumno/recurso/'+str(alumno.nombre_usuario)+'/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_post_alumno_imagen(client):    
    with api.app.app_context():
        directory_root = dirname(dirname(abspath(__file__)))
        path_img = os.path.join(str(directory_root),
                                "flaskr/uploads/categorias/default.jpg")
        
        with open(path_img, 'rb') as img_open:
            img = BytesIO(img_open.read())
            
            alumno = Alumno.objects().first()
            
            if alumno == None:
                assert True
            else:
                data = {
                    'imagen': (img, 'img.jpg')
                }
                rv = client.post('/alumno/imagen/'+str(alumno.id), content_type='multipart/form-data',data=data)
                if rv._status_code == 200:
                    assert True
                else:
                    assert False

def test_get_alumno_imagen(client):

    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/alumno/imagen/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_alumno_imagen_default(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/alumno/imagen/default/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_alumnos_curso(client):
    curso = Grado.objects().first()
    if curso == None:
        assert True
    else:
        rv = client.get('/alumnos/curso/'+str(curso.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False


def test_get_alumno_imagen_zoom(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/imagen/zoom/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_finalizar_tutorial(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/alumno/finalizar/tutorial/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False

def test_get_alumno_evaluaciones(client):
    alumno = Alumno.objects().first()
    if alumno == None:
        assert True
    else:
        rv = client.get('/alumno/evaluaciones/'+str(alumno.id))
        if rv._status_code == 200:
            assert True
        else:
            assert False