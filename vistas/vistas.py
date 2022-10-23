from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos import db, Tarea, Usuario
from modelos.modelos import TareaSchema, UsuarioSchema

tarea_schema = TareaSchema()
usuario_schema = UsuarioSchema()


class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(usuario=request.json["usuario"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}

class VistaTareas(Resource):   
    
    @jwt_required()
    def get(self):
        return [tarea_schema.dump(tarea) for tarea in Tarea.query.all()]

class VistaTarea(Resource):   
    
    @jwt_required()
    def get(self, id_tarea):
        return tarea_schema.dump(Tarea.query.get_or_404(id_tarea))    

    @jwt_required()
    def put(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        tarea.nuevo_formato = request.json.get("nuevo_formato", tarea.nuevo_formato)
        tarea.estado = request.json.get("estado", tarea.estado)
        db.session.commit()
        return tarea_schema.dump(tarea)
    
    @jwt_required()
    def delete(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        db.session.delete(tarea)
        db.session.commit()
        return '', 204

