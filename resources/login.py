from flask import Flask, Blueprint, jsonify, request, abort
from models.alumno import Alumno
from models.administrador import Administrador
from models.profesor import Profesor
from models.institucion import Institucion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from models.curso import Curso
import json
from flask_restful import reqparse

def init_module(api):
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(LoginColegio, '/login/colegio/<id>')
    api.add_resource(LoginApp, '/login/app')


class LoginColegio(Resource):
    def post(self,id):
        data = request.data.decode()
        data = json.loads(data)
        institucion = Institucion.objects(id=id).first()
        administrador = Administrador.objects(email = data['email'],institucion=institucion.id).first()
        profesor = Profesor.objects(email = data['email'],institucion=institucion.id).first()
        alumno = Alumno.objects(email = data['email'],institucion=institucion.id).first()
        if administrador != None :
            if(administrador.check_password(data['password']) or administrador.activo==False ):
                token = administrador.get_token()
                return {'respuesta':{'id':str(administrador.id)},
                            'tipo': 'ADMINISTRADOR', 
                            'token': str(token)
                        }
            else:
                return {'respuesta': 'no_existe'},401
        
        if profesor != None :
            if(profesor.check_password(data['password']) or administrador.activo==False):
                token = profesor.get_token()
                return {'respuesta':{'id':str(profesor.id)},
                            'tipo': 'PROFESOR', 
                            'token': str(token)
                        }
            else:
                return {'respuesta': 'no_existe'},401

        if alumno != None :
            if(alumno.check_password(data['password']) or administrador.activo==False):
                token = alumno.get_token()
                return {'respuesta':{'id':str(alumno.id)},
                            'tipo': 'ALUMNO', 
                            'token': str(token)
                        }
            else:
                return {'respuesta': 'no_existe'},401
        
        else:
            return {'respuesta': 'no_existe'},404
            

class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('password', type = str, required=True, location='json')
        self.reqparse.add_argument('tipo', type = str, default="ALUMNO", location='json')
        super(Login, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        email = args.get("email")
        passwd = args.get("password")
        tipo = args.get("tipo")
        recursos = []
        user = None
        if tipo == 'ALUMNO':
            user = Alumno.objects(email=email).first()
            for recurso in Curso.objects(alumnos__in=[user]).all(): 
                recursos.append(recurso.to_dict()) 
        elif tipo == 'ADMINISTRADOR':
            user = administrador = Administrador.objects(email=email).first()
        elif tipo == 'PROFESOR':
            user = Profesor.objects(email=email).first()
            for recurso in Curso.objects(profesor=user).all():
                recursos.append(recurso.to_dict())
        if user and user.activo and user.check_password(passwd):
            return {'respuesta':
                        {'id': str(user.id)},
                         'tipo': tipo,
                         'token': str(user.get_token()),
                         'recursos': recursos
                        }    
        return {'respuesta': 'no_existe'}, 401

class LoginApp(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, location='json')
        self.reqparse.add_argument('password', type = str, required=True, location='json')
        self.reqparse.add_argument('tipo', type = str, default="ALUMNO", location='json')
        super(LoginApp, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        email = args.get("email")
        passwd = args.get("password")
        tipo = args.get("tipo")

        user = None
        if tipo == 'ALUMNO':
            user = Alumno.objects(email=email).first()
        
        elif tipo == 'ADMINISTRADOR':
            user = Administrador.objects(email=email).first()

        elif tipo == 'PROFESOR':
            user = Profesor.objects(email=email).first()
        
        if user != None and user.activo and user.check_password(passwd):
                res = []
                if tipo == "ALUMNO":
                    res_bd = Curso.objects(alumnos__in=[user]).all()
                else:
                    res_bd = Curso.objects(profesor=user).all()
                for resource in res_bd:
                    res.append({
                        "id": str(resource.id),
                        "nombre": resource.nombre,
                        "fecha_creacion": resource.fecha_creacion.isoformat(),
                        "activo": resource.activo,
                        "version": resource.version,
                        "id_base": str(resource.curso_base.id),
                    })
                return {'respuesta': user.to_dict(),
                        'tipo': tipo, 
                        'token': str(user.get_token()),
                        'recursos': res
                       }
        return abort(403)
        

class Logout(Resource):
    def post(self):
        return {'respuesta': True}