from celery import Celery
import os
import timeit
from datetime import datetime 
celery_app = Celery(__name__,broker='redis://localhost:6379/0')
import os
from google.cloud import storage
import smtplib
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

sender = 'conversionesequipo28@gmail.com'
receivers = ['j.ballesterosv@uniandes.edu.co']
username = 'conversionesequipo28@gmail.com'
password = 'rgewrcxtqxjkgrrn'


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'CloudStorageCredentials.json'

client = storage.Client()
bucket = client.get_bucket('conversion-bucket-1')


# TODO(developer)
project_id = "noted-cider-367004"
subscription_id = "convertir-sub"
    #Number of seconds the subscriber should listen for messages
timeout = 5.0
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

@celery_app.task(name = 'registrar_log')
def encolar_tarea(filename,nuevo_formato,estado,taskid):
    status_update ='{"estado":"processed"}'
    nombreSinProcesar = filename.split(".")[0] + "_" + str(taskid) + "." + filename.split(".")[1]
    nombreProcesado = filename.split(".")[0] + "_" + str(taskid) + "." + nuevo_formato
    folderSinProcesar = "/home/josemani89/archivos_temporal/sin_procesar/{}".format(nombreSinProcesar)
    folderProcesados =  "/home/josemani89/archivos_temporal/procesados/{}".format(nombreProcesado)
    blob = bucket.blob(filename)
    blob.download_to_filename(folderSinProcesar)
    if (estado == "uploaded"):
        t = timeit.timeit(lambda: os.system('ffmpeg -i {} {} -y'.format(folderSinProcesar, folderProcesados)), number=1)
        blob = bucket.blob("sin_procesar/{}".format(nombreSinProcesar))
        blob.upload_from_filename(folderSinProcesar)        
        blob = bucket.blob("procesados/{}".format(nombreProcesado))
        blob.upload_from_filename(folderProcesados)
        #os.system('ffmpeg -i ../archivos_originales/{} ../archivos_procesados/{} -y'.format(filename,filename.split(".")[0]+"."+nuevo_formato))
        #os.system("curl -X PUT -H 'Content-Type: application/json' -d '{}' http://10.158.0.17:7001/tasks/{}".format(status_update,taskid))
        message = """Subject: Tarea de conversion completada correctamente

        Su tarea de conversion se ha completado correctamente, puede descargar el archivo dando clic en el siguiente link: 
        http://35.199.86.169:7001/descargaProcesado/123
        """
        smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        smtpObj.starttls()
        smtpObj.login(username, password)
        smtpObj.sendmail(sender, receivers, message) 
    with open ('logsw.txt', 'a+') as file:
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


### en caso de emergencia
#t = timeit.timeit(lambda: os.system('ffmpeg -i ../archivos_originales/{} ../archivos_procesados/{} -y'.format(filename,filename.split(".")[0]+"."+nuevo_formato)), number=1)
