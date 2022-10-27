from celery import Celery
import os 
celery_app = Celery(__name__,broker='redis://localhost:6379/0')

@celery_app.task(name = 'registrar_log')
def encolar_tarea(filename,nuevo_formato,estado):
    if (estado == "uploaded"):
        os.system('ffmpeg -i ../archivos_originales/{} ../archivos_procesados/{}'.format(filename,filename.split(".")[0]+"."+nuevo_formato))
