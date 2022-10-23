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

# class VistaTarea(Resource):

#     @jwt_required()
#     def get(self, id_tarea):
#         return tarea_schema.dump(Tarea.query.get_or_404(id_tarea))

#     @jwt_required()
#     def put(self, id_tarea):
#         carrera = Tarea.query.get_or_404(id_tarea)
#         carrera.nombre_carrera = request.json.get("nombre", carrera.nombre_carrera)
#         carrera.competidores = []

#         for item in request.json["competidores"]:
#             probabilidad = float(item["probabilidad"])
#             cuota = round((probabilidad / (1 - probabilidad)), 2)
#             competidor = Competidor(nombre_competidor=item["competidor"],
#                                     probabilidad=probabilidad,
#                                     cuota=cuota,
#                                     id_carrera=carrera.id)
#             carrera.competidores.append(competidor)

#         db.session.commit()
#         return carrera_schema.dump(carrera)

#     @jwt_required()
#     def delete(self, id_carrera):
#         carrera = Carrera.query.get_or_404(id_carrera)
#         db.session.delete(carrera)
#         db.session.commit()
#         return '', 204