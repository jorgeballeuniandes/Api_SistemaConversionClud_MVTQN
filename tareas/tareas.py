from celery import Celery
import os
import timeit
from datetime import datetime 
celery_app = Celery(__name__,broker='redis://localhost:6379/0')


@celery_app.task(name = 'registrar_log')
def encolar_tarea(filename,nuevo_formato,estado,taskid):
    status_update ='{"estado":"procesadosdas"}'
    nuevonombre = filename.split(".")[0]+"."+nuevo_formato
    
    if (estado == "uploaded"):
        t = timeit.timeit(lambda: os.system('ffmpeg -i ../archivos_originales/{} ../archivos_procesados/{} -y'.format(filename,filename.split(".")[0]+"."+nuevo_formato)), number=1)
        #os.system('ffmpeg -i ../archivos_originales/{} ../archivos_procesados/{} -y'.format(filename,filename.split(".")[0]+"."+nuevo_formato))
        os.system("curl -X PUT -H 'Content-Type: application/json' -d '{}' http://127.0.0.1:5000/tasks/{}".format(status_update,taskid))

    with open ('log_signin.txt', 'a+') as file:
        file.write ('Tarea id: {} - se procesó en {}s  \n'.format(taskid,t))              
        
        
#from celery import Celery
# celery_app = Celery(__name__,broker='redis://localhost:6379/0')

# @celery_app.task()
# def registrar_log(usuario, fecha):
#     with open ('log_signin.txt', 'a+') as file:
#         file.write ('{} - inicio de sesion:{}\n'.format(usuario, fecha))
                   
                   
                   #curl -X PUT -H 'Content-Type: application/json' -d '{"estado": "prosesado"}' http://172.17.0.3:7001/tasks/1


# open ('log_signin.txt', 'a+') as file:
#         file.write ('{} - inicio de sesion:{}\n'.format(usuario, fecha))


# t = timeit.timeit(lambda: 'os.system("fmpeg -i ~/Documents/Maestria/II_semestre/cloud_desarrollo/proyecto/test1.mpeg ~/Documents/Maestria/II_semestre/cloud_desarrollo/proyecto/test.11.mpeg")')



