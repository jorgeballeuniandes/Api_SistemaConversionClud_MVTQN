from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from os import getcwd
import os 
from modelos import db, Tarea, Usuario
from modelos.modelos import TareaSchema, UsuarioSchema
from datetime import datetime
from celery import Celery
import os
from google.cloud import storage
#from google.cloud import pubsub_v1

# project_id = "noted-cider-367004"
# topic_id = "convertir"


# publisher = pubsub_v1.PublisherClient()
# topic_path = publisher.topic_path(project_id, topic_id)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'CloudStorageCredentials.json'

client = storage.Client()
bucket = client.get_bucket('conversion-bucket-1')

# celery_app = Celery (__name__,broker = 'redis://10.158.0.4:6379/0' )
# @celery_app.task(name="registrar_log")
def registrar_log(*args):
    pass


tarea_schema = TareaSchema()
usuario_schema = UsuarioSchema()
PATH_FILE= getcwd

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

class Subir_archivos(Resource):
    @jwt_required()
    def post (self):
		
        file = request.files['file']
        file.save("/home/josemani89/archivos_temporal/{}".format(file.filename))
        blob = bucket.blob(file.filename)
        blob.upload_from_filename("/home/josemani89/archivos_temporal/{}".format(file.filename))


      
class Task_create(Resource):
    #@jwt_required()
    def post (self):
        nueva_tarea = Tarea(nombre_archivo = request.json["nombre_archivo"], nuevo_formato =request.json["nuevo_f"],time_stamp=datetime.utcnow(),estado="uploaded")
        db.session.add(nueva_tarea)
        db.session.commit()
        
        args=(request.json["nombre_archivo"],request.json["nuevo_f"],nueva_tarea.estado,nueva_tarea.id)
        registrar_log.apply_async(args=args, queue ='logs')
        data_str = "Message number"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        # future = publisher.publish(
        # topic_path, data,
        # filename=request.json["nombre_archivo"] ,nuevo_formato=request.json["nuevo_f"],estado=nueva_tarea.estado,taskid=str(nueva_tarea.id)
        # )
        #print(future.result())
        return {"mensaje": "la tarea se ha creado exitosamente", "Archivo": nueva_tarea.nombre_archivo, "formato": nueva_tarea.nuevo_formato, "id":nueva_tarea.id}

    
        

# class VistaTarea(Resource):
class VistaTareas(Resource):   
    
    @jwt_required()
    def get(self):
        return [tarea_schema.dump(tarea) for tarea in Tarea.query.all()]

class VistaTarea(Resource):   
    @jwt_required()
    def get(self, id_tarea):
        return tarea_schema.dump(Tarea.query.get_or_404(id_tarea))    

    #@jwt_required()
    def put(self, id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        tarea.nuevo_formato = request.json.get("nuevo_formato", tarea.nuevo_formato)
        tarea.nuevo_formato = request.json.get("nuevo_formato", tarea.nuevo_formato)
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
    
class Convertir(Resource):

    def post(self):
        
        for tarea in Tarea.query.all():
            if (tarea.estado == "uploaded"):
                os.system('ffmpeg -i ./archivos_originales/{} ./archivos_procesados/{}'.format(tarea.nombre_archivo,tarea.nombre_archivo.split(".")[0]+"."+tarea.nuevo_formato))
                tarea.estado = "processed"
                db.session.commit()
class CambioStado(Resource):
    def put(self,id_tarea):
        tarea = Tarea.query.get_or_404(id_tarea)
        tarea.estado = request.json.get("estado", tarea.estado)
        db.session.commit()
        return tarea_schema.dump(tarea)
        
            
