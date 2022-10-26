from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas import VistaSignIn, VistaLogIn,Task_create,Subir_archivos,Convertir 

from vistas import VistaSignIn, VistaLogIn
from vistas.vistas import VistaTareas, VistaTarea

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversiones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(Task_create,'/newTask')
api.add_resource(Subir_archivos,'/uploadFile')
api.add_resource(VistaSignIn, '/auth/signup')
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaTareas, '/tasks')
api.add_resource(VistaTarea, '/tasks/<int:id_tarea>')
api.add_resource(Convertir, '/convertir')


jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, port=7000, host='0.0.0.0')
