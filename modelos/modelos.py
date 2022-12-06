from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()





class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(128))
    nuevo_formato = db.Column(db.String(30))
    estado = db.Column(db.String(30))
    time_stamp = db.Column(db.String(30))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))




class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    email = db.Column(db.String(200))
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')





class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True
    time_stamp = fields.String()



class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True